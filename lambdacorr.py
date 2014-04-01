#! /usr/bin/env python

# lambdacorr.py
# ################
# Imported / Executed by iterate.py
#
# ################
# See White et al 1958, Chemical Equilibrium in Complex Mixtures for methodology
#  Performs lambda correction for TEA loop
#  MORE DOCSTRING

import numpy as np

import format as form
from TEA_config import *

def lambdacorr(it_num, datadir, doprint, direct=False):
    '''
    DOCSTRING
    '''
    # Supress nan warnings, as they are used for finding valid minima
    np.seterr(invalid='ignore')
    np.seterr(divide='ignore')
    
    # Read in values from header and previous non-corrected output
    #if bool(direct):
    input = direct
    #else:
    #    infile = datadir + '/lagrange-iteration-' + str(it_num) + '-nocorr.txt'
    #    input = form.readoutput(infile)
    
    header = input[0]
    pressure, temp, i, j, speclist, a, b, g_RT = form.readheader(header)
   
    y         = input[3]
    x         = input[4]
    delta     = input[5]
    y_bar     = input[6]
    x_bar     = input[7]
    delta_bar = input[8]

    # Perform checks to be safe
    it_num_check = input[1]
    speclist_check = input[2]
    
    check = np.array([
            it_num_check != it_num,
            False in (speclist_check == speclist) ])
    
    if check[0]:
        print("\n\nMAJOR ERROR! Read in file's it_num is not the current iteration!\n\n")
    
    if check[1]:
        print("\n\nMAJOR ERROR! Read in file uses different species order/list!\n\n")
    
    # Create 'c' value from 'g_RT' value with pressure correction    
    c = g_RT + np.log(pressure)
    
    # Set up eq(20) to find value of lambda
    def dF_dlam(s, i, x, y, delta, c, x_bar, y_bar, delta_bar):
        dF_dlam = 0
        for n in np.arange(i):
            dF_dlam += delta[n] * (c[n] + np.log(y[n] + s*delta[n]) - np.log(y_bar + s*delta_bar))
        return dF_dlam
    
    # Find an alternative or describe better
    repeat = True
    #lower  = -5
    #steps  =  10
    
    # ### READ ABOUT POSSIBLE BREAK!
    # If you ever get the error message "lam referenced before assignment",
    # here is what is happening. 
    # ---> This break is caused when the first check step makes it negative! <---
    # The the first "step" lambda correction takes to see if the mol numbers become 
    # negative is itself negative.
    # This means that lambdacorr can't find a "good" amount to step to get positive 
    # moles, so lambda correction essentially fails.
    # How to remedy this:
    # * Increase the magnitude of "lower." 
    # This will cause lambdacorr to try even smaller steps in order to ensure it
    # doesn't step too far. Doing so will increase computation time however as 
    # lambdacorr will have the navigate these new smaller steps every time, even
    # if it needs a "large" step instead.
    
    # ### Work-around for fsolve non-convergence given a far-off guess
    # Step towards final solution until negative masses are found
    # Use exponential exploration to ensure smaller steps do not overshoot 
    # negative masses
    
    # ### Create function to search dF_lam space for the last lambda value 
    # before the minimum is passed
    
    # Left To Right method, LTR
    def find_lam(range, i, x, y, delta, c, x_bar, y_bar, delta_bar):
        start = True
        for h in range:
            val = dF_dlam(h, i, x, y, delta, c, x_bar, y_bar, delta_bar)
#            if start & (val > 0 or np.isnan(val) == True):
            #print(val)
            if start & (val > 0 or np.isnan(val) == True):
                return False
            if val > 0 or np.isnan(val) == True:
                break
            lam = h
            start = False
        return lam
    
    # Right To Left method, RTL
    def find_lam2(range, i, x, y, delta, c, x_bar, y_bar, delta_bar):
        rev_range = range[::-1]
        for h in rev_range:
            val = dF_dlam(h, i, x, y, delta, c, x_bar, y_bar, delta_bar)
            #if val > 0 or np.isnan(val) == False:
            if val < 0 and np.isnan(val) == False:
                break
            old_val = val # val before stopping
            old_lam = h   # lam before stopping
        good_lam = h   # lam after stopping
        good_val = val # val after stopping
        return good_lam, old_lam#, good_val, old_val
    
    # ### Set up smart search for a good range of lambda to check: this will allow
    # lambdacorr to find correct ranges of value in order to prevent the error
    # outlined above; user input should no longer be required to fix this.
    
    range = np.exp(np.linspace(lower,0,steps))
    # FINDME: TESTING
    #print("At temp: " + str(temp))
    
    high_step = 0.05
    higher_lamb = np.arange(0.5, 1 + high_step, high_step)
    smart_range = np.append(range[range<0.5], higher_lamb)
    
    if explore:
        # Find close lambda left of critical point using RTL
        out_lam, old_lam = find_lam2(smart_range, i, x, y, delta, c, x_bar, y_bar, delta_bar)
        #print("Temperature:", temp)
        #print("RTL Previous lam:", old_lam)#, old_val)
        #print("RTL Good lam:", out_lam)#, val)
        
        # Add second explore to get even closer to good lambda using LTR
        near_range = np.linspace(out_lam, old_lam, steps)
        close_lam = find_lam(near_range, i, x, y, delta, c, x_bar, y_bar, delta_bar)
        #print("LTR Initial lam:", out_lam)
        #print("LTR Final lam:", close_lam)
        #print("\n")
    else:
        #for h in range:
        #    val = dF_dlam(h, i, x, y, delta, c, x_bar, y_bar, delta_bar)
        #    if val > 0 or np.isnan(val) == True:
        #        break
        #    lam = h
        #out_lam = lam
        #print("no explore")
        #print("  Trying lam: " + str(range[0]))
        close_lam = find_lam(range, i, x, y, delta, c, x_bar, y_bar, delta_bar)
        
    #print("    Good lam: " + str(out_lam))
    # Retrieve last lambda value before the minimum was passed
    lam = close_lam
    
    # OUTDATED, DO NOT USE
    # for h in range:
        # val = dF_dlam(h, i, x, y, delta, c, x_bar, y_bar, delta_bar)        
        # if val > 0 or np.isnan(val) == True:
                # break
        # lam   = h
    # 
    # print('final lambda:', lam)
    # print('bef:', dF_dlam(h, i, x, y, delta, c, x_bar, y_bar, delta_bar))
    # print('aft:', dF_dlam(lam, i, x, y, delta, c, x_bar, y_bar, delta_bar))   
    # '''
        # FINDME: fsolve convergence is failing.
        # result = fsolve(dF_dlam, lam, (i, x, y, delta, c, x_bar, y_bar, delta_bar), full_output=True)
        # if result[2] != 1:
            # step /= 10.
            # if doprint == True:
                # print('Lambda value of ' + np.str(lam) + ' was used unsuccessfully.')
                # print('Convergence was not found. Trying better precision...\n')
        # else:
            # repeat = False
            # lambda_it = result[0][0]
        # lambda_it = lam
            # if doprint == True:
                # print('Result converged; use lambda = ' + np.str(lambda_it))
                # repeat = False
    # '''
        
    # Correct x values given this value of lambda
    x_corr = y + lam * delta
    x_corr_bar = np.sum(x_corr)
    delta_corr = y - x_corr
    delta_corr_bar = x_corr_bar - y_bar
    
    #print("Previous y's:", y + old_lam * delta)
    #print("Good y's", y + out_lam * delta)
    
    # Export all values into output files or via memory
    #TESTING: ALWAYS WRITE FILES
    form.output(datadir, header, it_num, speclist, y, x_corr, delta_corr, y_bar, x_corr_bar, delta_corr_bar, doprint)
    form.fancyout(datadir, it_num, speclist, y, x_corr, delta_corr, y_bar, x_corr_bar, delta_corr_bar, doprint)
        
    #if direct:
    return [header, it_num, speclist, y, x_corr, delta_corr, y_bar, x_corr_bar, delta_corr_bar, doprint]
    #else:
    #    return False
    
# End of file
