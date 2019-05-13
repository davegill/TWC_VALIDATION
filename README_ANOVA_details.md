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

Let's consider multiple MPAS data sets to be _conformable_ if they all share the identical values for the following attributes:
   - mesh
   - vertical coordinate 
   - physics and dynamics run-time options
   - data output settings: stream, frequency, variable set
   
Assume that we have several conformable output data files. What statement can we make about the similarities or differences of the measured variables of these data sets?

We use an Analysis of Variance (ANOVA) test to look at multiple factors. Our null hypothesis is "these fields are the same". The ANOVA test provides a probability of rejecting that null hypothesis (a high probability means that we reject the null hypothesis, meaning we interpret the fields are different).

The measurements are the dependent variables. Our measurements are the values of `u`, `theta`, and `qv`. These values are specifically chosen from each of the levels of the `LOCATIONS` factor, each of the levels of the `TIMES` factor, and each of the levels of the `COMPILERS` factor. Within each of the `LOCATIONS`, we randomly choose a pre-selected number of points. For the three factors used in this experiment (assuming only two levels for each factor), we populate a table similar to what is shown below.
```
              -------------------------------------------------------------
              |           FACTOR 1          |          FACTOR 1           |
              |           Level 1           |          Level 2            |
              -------------------------------------------------------------
              |   FACTOR 2   |   FACTOR 2   |   FACTOR 2   |   FACTOR 2   |
              |   Level 1    |   Levels 2   |   Level 1    |   Level 2    |
---------------------------------------------------------------------------
              |              |              |              |              |
   FACTOR 3   |              |              |              |              |
   Level 1    |              |              |              |              |
              |              |              |              |              |
---------------------------------------------------------------------------
              |              |              |              |              |
   FACTOR 3   |              |              |              |              |
   Level 2    |              |              |              |              |
              |              |              |              |              |
---------------------------------------------------------------------------
```
Each of the empty boxes is filled with the measurements. Currently the number of measurements taken is set to 20 (a run-time configurable value). The measurements are the difference values (MPAS output - MPAS input) of the MPAS  variables. A table is constructed for each of the measured variables: `u`, `theta`, and `qv`, so three separate ANOVA tests are conducted.

After the ANOVA is conducted (three separate tests, one for each variable of interest: `u` (horizontal momentum, m/s), `theta` (potential temperature, K), and `qv` (water vapor mixing ratio, kg/kg). The typical ANOVA presentation is output to an auxiliary set of files. For example, here is the file `step_2_theta.txt`:
```
                  Source                   df      SS            MS   F Statistic
==================================================================================
                                 Mean    0001     0.00682     0.00682     0.792
                            LOCATIONS    0006    49.63231     8.27205   961.235
                            COMPILERS    0002     0.00009     0.00004     0.005
                                TIMES    0002     0.00110     0.00055     0.064
                LOCATIONS x COMPILERS    0012     0.00046     0.00004     0.004
                    LOCATIONS x TIMES    0012     6.93748     0.57812    67.179
                    COMPILERS x TIMES    0004     0.00004     0.00001     0.001
        LOCATIONS x COMPILERS x TIMES    0024     0.00012     0.00001     0.001
                                Error    1197    10.30096     0.00861
```
The three key factors are `LOCATIONS`, `COMPILERS`, and `TIMES`. We always and only care about the `F Statistic` for the `COMPILERS` factor. The other two factors are to make sure that we are not confounding the interpretation of our results. The probability of the given `F Statistic` is based on the degrees of freedom of the factor (here the `df` for `COMPILERS` is `0002`) and the degrees of freedom of the `Error` (here, `1197`). These three values, `0.005`, `0002`, and `1197` (the `F Statistic`, the degrees of freedom for the factor of interest, and the degrees of freedom for the `Error`) are sufficient to compute a probability.

A final python script is run to compute the probability of F Statistic. The result is interpreted as "What is the probability of rejecting the null hypotheis, i.e. rejecting the hypothesis that the fields are the same?"

   - A very high probability means that we DO reject the null hypothesis, that we DO interpret this field as different.
   - A very low probability means that we DO NOT reject the null hypothesis, that we DO interpret the field as similar.
