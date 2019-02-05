#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#STOLEN FROM
#https://stackoverflow.com/questions/38113120/calculate-f-distribution-p-values-in-python

#	If you have an f statistic, and you want to know a probability

import math

def incompbeta(a, b, x):

    ''' incompbeta(a,b,x) evaluates incomplete beta function, here a, b > 0 and 0 <= x <= 1. This function requires contfractbeta(a,b,x, ITMAX = 200) 
    (Code translated from: Numerical Recipes in C.)'''

    if (x == 0):
        return 0;
    elif (x == 1):
        return 1;
    else:
        lbeta = math.lgamma(a+b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1-x)
        if (x < (a+1) / (a+b+2)):
            return math.exp(lbeta) * contfractbeta(a, b, x) / a;
        else:
            return 1 - math.exp(lbeta) * contfractbeta(b, a, 1-x) / b;

def contfractbeta(a,b,x, ITMAX = 200):

    """ contfractbeta() evaluates the continued fraction form of the incomplete Beta function; incompbeta().  
    (Code translated from: Numerical Recipes in C.)"""

    EPS = 3.0e-7
    bm = az = am = 1.0
    qab = a+b
    qap = a+1.0
    qam = a-1.0
    bz = 1.0-qab*x/qap

    for i in range(ITMAX+1):
        em = float(i+1)
        tem = em + em
        d = em*(b-em)*x/((qam+tem)*(a+tem))
        ap = az + d*am
        bp = bz+d*bm
        d = -(a+em)*(qab+em)*x/((qap+tem)*(a+tem))
        app = ap+d*az
        bpp = bp+d*bz
        aold = az
        am = ap/bpp
        bm = bp/bpp
        az = app/bpp
        bz = 1.0
        if (abs(az-aold)<(EPS*abs(az))):
            return az

    print 'a or b too large or given ITMAX too small for computing incomplete beta function.'


try:
    F=float(raw_input('Input, F-statistic: '))
    print F
except ValueError:
    print "Not a number"

try:
    df1=int(raw_input('Input, df factor: '))
    print df1
except ValueError:
    print "Not a number"

try:
    df2=int(raw_input('Input, df error: '))
    print df2
except ValueError:
    print "Not a number"

print ("p-value probability = 1.0 means 100% reject null hypothesis that means are same")
print ("p-value probability = " + str(incompbeta(.5*df1, .5*df2, float(df1)*F/(df1*F+df2))) )
if incompbeta(.5*df1, .5*df2, float(df1)*F/(df1*F+df2)) < 0.10 :
    print ("\nWe are pretty darn confident that our comparisons are OK")
    print (" " )
    print ("            ▕▔▔▔╲ ")
    print ("             ▏  ▕ ")
    print ("             ▏  ▕ ")
    print ("             ▏  ▕ ")
    print ("             ▏  ▕▂▂▂▂")
    print ("      ▂▂▂▂▂▂╱┈▕      ▏")
    print ("      ▉▉▉▉▉┈┈┈▕▂▂▂▂▂▂▏")
    print ("      ▉▉▉▉▉┈┈┈▕      ▏")
    print ("      ▉▉▉▉▉┈┈┈▕▂▂▂▂▂▂▏")
    print ("      ▉▉▉▉▉┈┈┈▕      ▏")
    print ("      ▉▉▉▉▉┈┈┈▕▂▂▂▂▂▂▏")
    print ("      ▉▉▉▉▉╲┈┈▕      ▏")
    print ("      ▔▔▔▔▔▔╲▂▕▂▂▂▂▂▂▏")
    print (" " )
    print (" " )
elif incompbeta(.5*df1, .5*df2, float(df1)*F/(df1*F+df2)) > 0.90 :
    print (" " )
    print ("\nThere are DEFINITELY problems with the GPU comparison")
    print (" " )
    print ("                ▉▉▉▉▉▉▉▉▉▉▉")
    print ("            ▉▉▉              ▉▉")
    print ("         ▉▉                   ▉▉ ")
    print ("        ▉▉     ▉▉        ▉▉     ▉ ")
    print ("     ▉▉        ▉▉▉       ▉▉▉     ▉▉ ")
    print ("    ▉▉                            ▉▉ ")
    print ("   ▉▉                            ▉▉ ")
    print ("  ▉▉          ▉▉▉▉▉▉▉▉▉          ▉▉ ")
    print ("  ▉▉       ▉▉           ▉▉       ▉▉ ")
    print ("  ▉▉      ▉               ▉     ▉▉")
    print ("  ▉▉▉                         ▉▉")
    print ("   ▉▉▉                      ▉▉")
    print ("    ▉▉▉                    ▉▉")
    print ("        ▉▉             ▉▉▉")
    print ("          ▉▉▉▉▉▉▉▉▉▉▉")
    print (" " )
    print (" " )
else:
    print (" " )
    print ("\nWe expect the probability to be < 0.10")
    print ("This error is larger than we typically see")
    print ("We probably need to look at plots of the data")
    print (" " )
    print ("             ▉▉▉▉▉▉▉▉          ")
    print ("        ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉       ")
    print ("      ▉▉▉▉▉▉▉▉     ▉▉▉▉▉▉▉▉    ")
    print ("     ▉▉▉▉▉            ▉▉▉▉▉▉   ")
    print ("     ▉▉▉▉              ▉▉▉▉▉   ")
    print ("                       ▉▉▉▉▉   ")
    print ("                    ▉▉▉▉▉▉▉    ")
    print ("                 ▉▉▉▉▉▉▉       ")
    print ("               ▉▉▉▉▉▉▉         ")
    print ("              ▉▉▉▉▉            ")
    print ("             ▉▉▉▉▉             ")
    print ("             ▉▉▉▉▉             ")
    print ("             ▉▉▉▉▉             ")
    print ("             ▉▉▉▉▉             ")
    print ("                               ")
    print ("             ▉▉▉▉              ")
    print ("             ▉▉▉▉              ")
    print (" " )
    print (" " )
