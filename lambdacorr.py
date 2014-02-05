# LAMBDACORR.PY
# Executed by iterate.py

#print('Lambdacorr imports...')
import numpy as np
#from sys import argv
#from sympy.solvers import solve
#from scipy.optimize import fsolve
#import matplotlib.pylab as plt
#import os
#os.environ['OMP_NUM_THREADS']='10'
import format as form


def lambdacorr(it_num, datadir, doprint, direct=False, fromatm=False, dex=False):
    '''
    DESC HERE
    '''
    np.seterr(all='ignore')
    # File name is from command terminal
    infile = datadir + '/lagrange-iteration-' + str(it_num) + '-nocorr.txt'
    
    # ### ONLY FOR IN-LINE TESTING
    '''
    ext = "C:\Users\Nestor\My Work\ESP 01\TEA\\"
    infile = ext + infile
    '''
    
    # ### Read in values from header.txt and previous no-corrected output
    if bool(direct):
        input = direct
    else:
        input = form.readoutput(infile)
    
    header = input[0]
    pressure, temp, i, j, speclist, a, b, c = form.readheader(header, fromatm, dex)
    
    y         = input[3]
    x         = input[4]
    delta     = input[5]
    y_bar     = input[6]
    x_bar     = input[7]
    delta_bar = input[8]
    
    # FINDME
    #b *= 10
    
    
    # ### Perform checks to be safe
    it_num_check = input[1]
    speclist_check = input[2]
    
    check = np.array([
            it_num_check != it_num,
            False in (speclist_check == speclist) ])
    
    if check[0]:
        print("\n\nMAJOR ERROR! Read in file's it_num is not the current iteration!\n\n")
    
    if check[1]:
        print("\n\nMAJOR ERROR! Read in file uses different species order/list!\n\n")
    
    # Correct 'c' for pressure
    c = c + np.log(pressure)
    
    # ### Set up eq(20) to find value of lambda
    def dF_dlam(s, i, x, y, delta, c, x_bar, y_bar, delta_bar):
        dF_dlam = 0
        for n in np.arange(i):
            dF_dlam += delta[n] * (c[n] + np.log(y[n] + s*delta[n]) - np.log(y_bar + s*delta_bar))
        return dF_dlam
    
    # ### vvv Find an alternative or describe better vvv
    repeat = True
    lower  = -20
    steps  = 30
    
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
    
    # Work-around for fsolve non-convergence given a far-off guess
    #while repeat == True:
    range = np.exp(np.linspace(lower, 0, steps))
    for h in range:
        val = dF_dlam(h, i, x, y, delta, c, x_bar, y_bar, delta_bar)
        if val > 0 or np.isnan(val) == True:
            break
        lam = h
        val_old = val
            
            #print(dF_dlam(range, i, x, y, delta, c, x_bar, y_bar, delta_bar))
            #plt.savefig('image.png')
            #repeat = False
        '''
        result = fsolve(dF_dlam, lam, (i, x, y, delta, c, x_bar, y_bar, delta_bar), full_output=True)
        if result[2] != 1:
            step /= 10.
            if doprint == True:
                print('Lambda value of ' + np.str(lam) + ' was used unsuccessfully.')
                print('Convergence was not found. Trying better precision...\n')
        else:
            repeat = False
            lambda_it = result[0][0]
        #lambda_it = lam
            if doprint == True:
                print('Result converged; use lambda = ' + np.str(lambda_it))
                repeat = False
        '''
    #print(lam)
    lambda_it = lam  
    # ### Correct x values given this value of lambda
    x_corr = y + lambda_it * delta
    x_corr_bar = np.sum(x_corr)
    delta_corr = y - x_corr
    delta_corr_bar = x_corr_bar - y_bar
        
    # ### Export all values into output files
    if direct:
        return [header, it_num, speclist, y, x_corr, delta_corr, y_bar, x_corr_bar, delta_corr_bar, doprint]
    else:
        form.output(datadir, header, it_num, speclist, y, x_corr, delta_corr, y_bar, x_corr_bar, delta_corr_bar, doprint)
        form.fancyout(datadir, it_num, speclist, y, x_corr, delta_corr, y_bar, x_corr_bar, delta_corr_bar, doprint)
        return False
    
