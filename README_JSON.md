#### TWC_VALIDATION ####

This README file explains how to set up the run-time configuration file `input.json`. This file is input by the `rd_n_wrt.py` script.

1. JSON files do not permit explanatory comments. There is a provided entry for an overall comment.
```
	"_comment_" : "Example of three files nearly the same, all PASS",
```

2. To verify that the input in the JSON file is getting into the `rd_n_wrt.py` script, this flag can be set to `true`. 
```
	"debug"       :   false,
```

3. Here is a list of files that will be considered:
```
> ls -ls /gpfs/fs1/p/mmm/wmr/gill/TWC_60km/
3843952 -rw-r--r-- 1 gill nmmm0048 3936197352 Feb  4 17:44 restart.2010-10-24_00.00.00.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.06.00_A_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.06.00_B_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.06.00_C_michael.nc
 394256 -rw-r--r-- 1 gill nmmm0048  403710928 Feb  4 17:43 validation.2010-10-24_00.06.00_D_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.12.00_A_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.12.00_B_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.12.00_C_michael.nc
 394256 -rw-r--r-- 1 gill nmmm0048  403710928 Feb  4 17:43 validation.2010-10-24_00.12.00_D_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.18.00_A_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.18.00_B_michael.nc
 358416 -rw-r--r-- 1 gill nmmm0048  367010192 Feb  4 17:43 validation.2010-10-24_00.18.00_C_michael.nc
 394256 -rw-r--r-- 1 gill nmmm0048  403710928 Feb  4 17:43 validation.2010-10-24_00.18.00_D_michael.nc
```

Set `mpas_root` to include the PATH and the portion of the FILENAME before the DATE. *This needs to be modified for a particular case.*
```
	"mpas_root"   :   "/gpfs/fs1/p/mmm/wmr/gill/TWC_60km/validation",
```

The `mpas_tail` is the common part of the file name AFTER the date and AFTER the TEST type. *This needs to be modified for a particular case.*
```
	"mpas_tail"   :   "_michael.nc",
```

The `init_file` is either the inital condition file or a restart. It is the full PATH and FILENAME. *This needs to be modified for a particular case.*
```
	"init_file"   :   "/gpfs/fs1/p/mmm/wmr/gill/TWC_60km/restart.2010-10-24_00.00.00.nc",
```

4. Part of the test is to choose a number of geophysical regions. Within each region, how many points are sampled.
```
	"num_points_per_region" : 20,
```

5. The comparison is made with these specific variables, at these specific levels. The field `u` is the horizontal momentum, m/s. The vertical level associated with this variable is 40, where the Vertical Level is 0-based (`v_lev_0_based`) means that the level near the surface of the earth is defined as `0`. The other two fields are `qv` (water vapor mixing ratio, kg/kg), and `theta` (potential temperature, K). It is beneficial to sample fields at different levels to make sure that the entire atmosphere is checked for differences. These values should not be modified.
```
	"compare" : [ 
		{
			"field" : "u" , 
			"v_lev_0_based" : 40
		},

		{
			"field" : "qv" , 
			"v_lev_0_based" : 2
		},

		{
			"field" : "theta" , 
			"v_lev_0_based" : 0
		}
	],
```

6. This portion defines the three factors for this three-way ANOVA: geophysical locations, the hardware / software comparison, and the time levels of the model output. 

   - The `LOCATIONS` should not be randomly be changed. These were selected to represent different hemispheres, elevations, day / night periods on the globe, tropical vs polar, desert vs ocean, etc. 
```
		{
			"factor" : "LOCATIONS",
			"names"  : [ "Indian", "Pacific", "Himilaya", "Sahara", "Australia", "Rockies", "Antarctic" ],
			"levels" : [ "Indian Ocean", "East Pac Tropical", "Himilayan Mtns", 
			             "Sahara Desert", "Australian Desert", "Rocky Mtns", "Antarctica" ]
		},
```

   - The `COMPILERS` factor is the generic name given to the actual comparison test of interest. For example, different levels of optimzations, CPU vs GPU, a collection of compilers, etc. These names (here, `A`, `B`, and `C`) need to match the strings AFTER the DATE in the MPAS model output FILENAMES. *This needs to be modified for a particular case.*
```
		
		{
			"factor" : "COMPILERS",
			"names"  : [ "A", "B", "C" ],
			"levels" : [ "A", "B", "C" ] 
		},
```

   - The `TIMES` factor should ALWAYS be the first three time steps of the simulation (either after the restart of after the initialization).  The `levels` of the `TIMES` need to exactly match the strings in the MPAS model output FILENAMES.
```
		
		{
			"factor" : "TIMES",
			"names"  : [ "06 min", "12 min", "18 min" ],
			"levels" : [ "2010-10-24_00.06.00", "2010-10-24_00.12.00", "2010-10-24_00.18.00" ]
		}
	],
```

7. Associated with the `LOCATIONS` and the latitude / longitude boxes that define that area. These are not necessarily the same size. These should not be changed.
```
	"min_lat_box_degrees" : [ -4,   -5, 29, 17, -29,   30,  -89.9 ],
	"max_lat_box_degrees" : [  4,    5, 42, 28, -20,   50,  -84.0 ],
	"min_lon_box_degrees" : [ 56, -170, 70, -4, 124, -110, -179.9 ],
	"max_lon_box_degrees" : [ 70, -110, 88, 27, 144, -105,  179.9 ],
```

8. A generic random seed to allow reproducible pseudo-random results. This does not need to be changed.
```
	"random_seed" : 9001
```
