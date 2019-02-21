#!/bin/csh

#	Did the user specify a JSON file for input.

if ( ${#argv} == 1 ) then
	set JSON_FILE = $1
else
	set JSON_FILE = input.json
endif

#	Does the input JSON file exist?

if ( ! -e input.json ) then
	echo "The $JSON_FILE does not exist"
	exit ( 1 ) 
endif

#	Clean up old files that might be laying around.

if ( -e step_1.out ) then
	rm -rf step_1.out >& /dev/null
	rm -rf step_2*.out >& /dev/null
	rm -rf theta.txt qv.txt u.txt >& /dev/null
endif

echo ; echo running python script to construct differences
python rd_n_wrt.py $JSON_FILE >& step_1.out

if ( ( ! -e theta.txt ) || \
     ( ! -e     u.txt ) || \
     ( ! -e    qv.txt ) ) then
	echo "The initial python script failed:"
	echo
	cat step_1.out
	echo
	echo "The initial python script failed:"
	exit ( 2 )
endif

#	Build Fortran code that computes ANOVA statistics

make -s anova

#	Run ANOVA tests on fields

set vars_to_test = `grep '"field"' $JSON_FILE | cut -d'"' -f4`

foreach v ( $vars_to_test )

	#echo ; echo use that input for ANOVA for $v
	./anova < ${v}.txt | tail -12 > step_2_${v}.out

	echo ; echo compiler comparison for $v
	f2p.py < fort.10

end

#	Clean up

rm fort.10
