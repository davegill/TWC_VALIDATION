anova : anova.f90
	gfortran -o anova -g -O0 -fbacktrace -ggdb -fcheck=bounds,do,mem,pointer -ffpe-trap=invalid,zero,overflow -ffree-line-length-none anova.f90

clean : 
	\rm -f anova stats.mod support.mod

superclean : clean
	\rm -f region_lat_lon.txt step_1.out step_2_theta.out step_2_u.out support.mod theta.txt u.txt
