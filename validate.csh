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

echo ; echo use that input for ANOVA for theta
make
./anova < theta.txt | tail -12 > step_2_theta.out

echo ; echo compiler comparison for theta
f2p.py < fort.10

echo ; echo use that input for ANOVA for qv
make
./anova < qv.txt | tail -12 > step_2_qv.out

echo ; echo compiler comparison for qv
f2p.py < fort.10

echo ; echo use that input for ANOVA for u
./anova < u.txt     | tail -12 > step_2_u.out

echo ; echo compiler comparison for u
f2p.py < fort.10
rm fort.10
