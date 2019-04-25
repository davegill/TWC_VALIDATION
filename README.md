## TWC_VALIDATION ##

The purpose of the TWC_VALIDATION code is to provide an objective evaluation of the _sameness_ of the output from different MPAS simulations. With this validation test, we expect the results to be nearly identical. The statistical technique that will be used in this test is typically part of an analysis associated with the Design of Experiments. In keeping with a systematic approach to causal impact, specific independent variables are manipulated and the resulting impacts on the dependent variables are determined. For the necessity of statistical rigor, randomization is included in the process.

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

1. Fill in the run-time configuration file, `input.json`. There is a `README_JSON.md` file with specific details. There is an `EXAMPLES` directory that has several JSON files that are set up to work on NCAR's cheyenne computer.
2. Run the driver script `validate.csh`, no arguments required as everything comes in from the JSON file.
3. This script has three parts:
   a. Read the NETCDF MAPS model data, select the correct variables and geophysical locations, compute differences, output temporary text files for use by the ANOVA program
   b. Run a three-factor ANOVA test on the following variables: u (horizontal momentum), t (potential temperature), qv (water vapor mixing ratio)
   c. Interpret the ANOVA output to produce a probability.

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
2. Very confident that the results are different. For this variable, this is considered a NEGATIVE indiactor that this field is the same. To assume this response, we need any single variable to display to disply this symbol:
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
3. Gray area, just not sure. This is an indeterminate region. This is the state when there are no NEGATIVE indicators, but there are also no all POSITIVE indicators.
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
