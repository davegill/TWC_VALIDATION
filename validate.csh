#!/bin/csh

echo ; echo running python script to construct differences
python rd_n_wrt.py input.json >& step_1.out

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
