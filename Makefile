anova : anova.f90
	gfortran -o anova -g -O0 -fbacktrace -ggdb -fcheck=bounds,do,mem,pointer -ffpe-trap=invalid,zero,overflow -ffree-line-length-none -fdefault-real-8 anova.f90

clean : 
	\rm -f anova stats.mod support.mod
	\rm -f step_1.out
	\rm -f step_2_qv.out step_2_theta.out step_2_u.out

superclean : clean
	\rm -f region_lat_lon.txt step_1.out support.mod
	\rm -f step_2_theta.out theta.txt
	\rm -f step_2_u.out u.txt
	\rm -f step_2_qv.out qv.txt
