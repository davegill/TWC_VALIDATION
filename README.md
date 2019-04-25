## TWC_VALIDATION ##

The purpose of the TWC_VALIDATION code is to provide an objective evaluation of the _sameness_ of the output from different MPAS simulations. With this validation test, we expect the results to be nearly identical. 

#### Example Uses for this Code ####

   - Comparing the output from same the code run with different compilers
   - Comparing the output from same the code run with different optimzation levels of the same compiler
   - Comparing the output from same the code run with different versions of the same compiler
   - Comparing the output from same the code run with different hardware
   - Comparing the output from same the code run with different floating point precision

#### Incorrect Uses for this Code ####

   - Comparing the output from different physics schemes
   - Comparing the output from different dynamics options
   - Comparing the output from different meshes
   - Comparing the output from different horizontal or vertical resolution

#### How To Run #### 

1. Fill in the run-time configuration file, `input.json`. There is a `README_JSON.md` file with specific details. 
2. The scripting system does not work with python 3 (yet). It is known to work with python/2.7.13. The following python modules are required:
   - numpy
   - netcdf4-python
   - scipy
   - matplotlib
3. To try out this system on the NCAR cheyenne environment, there is an `EXAMPLES` directory that has several JSON files that are set up to work specifically on cheyenne. This syntax is sufficient for cheyenne.
```
> ml python/2.7.13 
> ml numpy 
> ml netcdf4-python 
> ml scipy 
> ml matplotlib
```
4. Run the executable driver script `./validate.csh`, no arguments required as everything comes in from the JSON file.
5. This script has three parts:
    - Read the NETCDF MAPS model data, select the correct variables and geophysical locations, compute differences, output temporary text files for use by the ANOVA program
    - Run a three-factor ANOVA test on the following variables: `u` (horizontal momentum), `theta` (potential temperature), and `qv` (water vapor mixing ratio)
    - Interpret the ANOVA output to produce a probability.

#### How To Interpret Results ####

For ease of use, the results are broken into three pieces: 
1. Very confident that the results are the same. For this variable, this is considered a POSITIVE indicator that this field is the same. To assume that response, we need all three variables to display this symbol:
```
                ▕▔▔▔╲ 
                 ▏  ▕ 
                 ▏  ▕ 
                 ▏  ▕ 
                 ▏  ▕▂▂▂▂
          ▂▂▂▂▂▂╱┈▕      ▏
          ▉▉▉▉▉┈┈┈▕▂▂▂▂▂▂▏
          ▉▉▉▉▉┈┈┈▕      ▏
          ▉▉▉▉▉┈┈┈▕▂▂▂▂▂▂▏
          ▉▉▉▉▉┈┈┈▕      ▏
          ▉▉▉▉▉┈┈┈▕▂▂▂▂▂▂▏
          ▉▉▉▉▉╲┈┈▕      ▏
          ▔▔▔▔▔▔╲▂▕▂▂▂▂▂▂▏
```
2. Very confident that the results are different. For this variable, this is considered a NEGATIVE indiactor that this field is the same. To assume this response, we need any single variable to display to display this symbol:
```
                    ▉▉▉▉▉▉▉▉▉▉▉
                ▉▉▉              ▉▉
             ▉▉                   ▉▉ 
            ▉▉     ▉▉        ▉▉     ▉ 
         ▉▉        ▉▉▉       ▉▉▉     ▉▉ 
        ▉▉                            ▉▉ 
       ▉▉                            ▉▉ 
      ▉▉          ▉▉▉▉▉▉▉▉▉          ▉▉ 
      ▉▉       ▉▉           ▉▉       ▉▉ 
      ▉▉      ▉               ▉     ▉▉
      ▉▉▉                         ▉▉
       ▉▉▉                      ▉▉
        ▉▉▉                    ▉▉
            ▉▉             ▉▉▉
              ▉▉▉▉▉▉▉▉▉▉▉
```
3. Gray area, just not sure. This is an indeterminate region. This is the state when there are no NEGATIVE indicators, but there are also not all POSITIVE indicators.
```
                 ▉▉▉▉▉▉▉▉          
            ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉       
          ▉▉▉▉▉▉▉▉     ▉▉▉▉▉▉▉▉    
         ▉▉▉▉▉            ▉▉▉▉▉▉   
         ▉▉▉▉              ▉▉▉▉▉   
                           ▉▉▉▉▉   
                        ▉▉▉▉▉▉▉    
                     ▉▉▉▉▉▉▉       
                   ▉▉▉▉▉▉▉         
                  ▉▉▉▉▉            
                 ▉▉▉▉▉             
                 ▉▉▉▉▉             
                 ▉▉▉▉▉             
                 ▉▉▉▉▉             
                                   
                 ▉▉▉▉              
                 ▉▉▉▉              
```
