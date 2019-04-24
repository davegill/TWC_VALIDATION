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

#### The Big Picture ####

Let's start with some concrete associations and examples.

Two of the independent variables that are considered include the geographical location (for example, Indian Ocean vs the Rocky Mountains vs Central Australia), and the time level of the model output (for example, time step _n_ vs time step _n+1_). The third independent variable is typically the specific factor that we want to consider (for example, GNU vs PGI vs Intel compilers). A full comparison requires that each setting of these independent variables (factors) is matched with every possible combination of the other (factors). The necessary comparisons for the example setup would include:
   - Indian Ocean with time step _n_ with GNU
   - Indian Ocean with time step _n_ with PGI
   - Indian Ocean with time step _n_ with Intel
   - Indian Ocean with time step _n+1_ with GNU
   - Indian Ocean with time step _n+1_ with PGI
   - Indian Ocean with time step _n+1_ with Intel
   - Rocky Mountains with time step _n_ with GNU
   - Rocky Mountains with time step _n_ with PGI
   - Rocky Mountains with time step _n_ with Intel
   - Rocky Mountains with time step _n+1_ with GNU
   - Rocky Mountains with time step _n+1_ with PGI
   - Rocky Mountains with time step _n+1_ with Intel
   - Central Australia with time step _n_ with GNU
   - Central Australia with time step _n_ with PGI
   - Central Australia with time step _n_ with Intel
   - Central Australia with time step _n+1_ with GNU
   - Central Australia with time step _n+1_ with PGI
   - Central Australia with time step _n+1_ with Intel

This type of design is referred to as a _three factor_ experiment (we have three factors: location, time level, and the hardware / software settings). Each factor has two or more levels (for example, the location factor has Indian Ocean, the Rocky Mountains, and Central Australia levels).

The response variables (the dependent variables) are the measured quantities. For the validation testing, the fundamental variables for horizontal momentum, temperature, and moisture constitute the entire comparison. We normalize the response variables to only look at a perturbation from an "expected" value, which tends to provide a zero bias. This is not necessary, but just a convenience.

Two data sets are conformable if they share the identical values for the following attributes:
   - mesh
   - vertical coordinate 
   - physics and dynamics run-time options
   - data output settings: frequency, variable set
   

Assume that we have several conformable output data files. What statement can we make about the similarities or differences of these data sets?
