#! /usr/bin/env python

# ITERATE.PY
# In-shell inputs: header file, data directory, True/False printing
#
# FOR TESTING
'''
python iterate.py full_White2.txt testing2 False
'''
# NOTE! Precision is used as follows:
# precision = 1e-(exp), so that
# if exp = 1, precision = 1e-1 = 0.1
#    exp = 5, precision = 1e-5 = 0.00001
# This is used for the program to know when no improvement is made on
#  the mol numbers from repeated lagrangian minimizations. A higher 'exp'
#  value will result in more iterations being run.
#
# NOTE!!!!! fromatm, dex=True must also be in lagrange and lambacorr right now!

# How abundances are read from input
dex      = False      # Read as fromatm, dex values, log_10(counts)
massfrac = False     # Read as mass fraction
molefrac = False     # Read as mole fraction

# Clean will remove files after use, but still create them to read/write 
# between iterations.  To stop use of files all together, use nofile.
# Note that speed increases if nofile is used, and multiple temp / pressure
# values will ONLY run with nofile.
# To read from atm file instead of header, set fromatm = True.  This is the only way
# run TEA over a list of T/P points
clean   = True
nofile  = True
fromatm = False
maxiter = 100 # Iteration to stop at
exp     = 40  # Precision in decimal places required for completion
# Above 9 on linux will loop forever?
# Up to 14 due to float constraints


# #################### NO EDITTING BELOW THIS LINE #################### #

#print("Iterate imports...")
#import numpy as np
from numpy import size
from numpy import where
from multiprocessing import Process, Queue
#from sys import stdout
from sys import argv
from sys import stdout
from ast import literal_eval
#from sympy.core    import Symbol
#from sympy.solvers import solve

import lagrange   as lg
import lambdacorr as lc
import format     as form
from   format import printout

# Read run-time arguments
header   = argv[1:][0] # name of header file
datadir  = 'outputs/' + argv[1:][1] # location of storage directory
datadirr = 'results/' + argv[1:][1] # location of final results
doprint  = literal_eval(argv[1:][2])

# Retrieve and set header info
inhead   = form.readheader(header, fromatm, dex)
pressure = inhead[0]
temp     = inhead[1]
precision = 10**(-exp)

# Retrieve and set initial values of x
infile = datadir + '/lagrange-iteration-0.txt'
input  = form.readoutput(infile)
speclist  = input[2]
x         = input[3]
x_old     = x
x_bar     = input[6]
x_bar_old = x_bar


# ### Setup up first iteration (always has to be at least 1 iteration)
it_num  = 1
repeat  = True
fullout = True

# ### Prepare iterative process to accept either files or pass data in memory
if nofile:
    fin_iter2 = [header, 0, speclist, x, x, 0, x_bar, x_bar, 0]
else:
    fin_iter2 = False

while (repeat & fullout):
    # Simple progress info
    if not doprint:
        stdout.write(' ' + str(it_num) + '\r')
        stdout.flush()
        
    # ### Perform 'starting' iteration
    ini_iter = lg.lagrange(it_num, datadir, doprint, fin_iter2, fromatm, dex)
    
    # ### Cleanup files that are no longer needed
    form.cleanup(datadir, it_num, clean)
    
    if doprint:
        printout('Iteration %d Lagrange complete. Starting lambda correction...', it_num)
    
    if fin_iter2:
        lag_dat, lag_dat2 = ini_iter[4], ini_iter[7]
    else:
        temp_in = form.readoutput(datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt")
        lag_dat, lag_dat2 = temp_in[4], temp_in[7]
        
    #[header, it_num, speclist, y, x, 
    #  delta, y_bar, x_bar, delta_bar] = lg.lagrange(it_num, datadir, doprint)
    
    if where((lag_dat < 0) == True)[0].size != 0:
        if doprint:
            printout('Correction required. Initializing...')
        ini_iter2 = lc.lambdacorr(it_num, datadir, doprint, ini_iter, fromatm, dex)
        if doprint:
            printout('Iteration %d lambda correction complete. Checking precision...', it_num)
    else:
        if fin_iter2:
            ini_iter2 = ini_iter
            if doprint:
                printout('Iteration %d did not need lambda correction.', it_num)
        else:
            prev = datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt"
            prev_load = open(prev)
            next = datadir + "/lagrange-iteration-" + str(it_num) + ".txt"
            next_load = open(next, 'w')
            data = prev_load.read()
            next_load.write(data)
            prev_load.close()
            next_load.close()
            if doprint:
                printout('Iteration %d did not need lambda correction.', it_num)
    
    # ### Perform 'next' iteration
    it_num += 1
    
    # Simple progress info
    if not doprint:
        stdout.write(' ' + str(it_num) + '\r')
        stdout.flush()
    
    fin_iter = lg.lagrange(it_num, datadir, doprint, ini_iter2, fromatm, dex)
    if doprint:
        printout('Iteration %d Lagrange complete. Starting lambda correction...', it_num)
    
    # ### Cleanup files that are no longer needed
    form.cleanup(datadir, it_num, clean)
    
    if fin_iter2:
        lag_dat = fin_iter[4]
    else:
        lag_dat = form.readoutput(datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt")[4]
    
    if where((lag_dat < 0) == True)[0].size != 0:
        if doprint:
            printout('Correction required. Initializing...')
        fin_iter2 = lc.lambdacorr(it_num, datadir, doprint, fin_iter, fromatm, dex)
        if doprint:
            printout('Iteration %d lambda correction complete. Checking precision...', it_num)
        
    else:
        if fin_iter2:
            fin_iter2 = fin_iter
            if doprint:
                printout('Iteration %d did not need lambda correction.', it_num)
        else:
            prev = datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt"
            prev_load = open(prev)
            next = datadir + "/lagrange-iteration-" + str(it_num) + ".txt"
            next_load = open(next, 'w')
            data = prev_load.read()
            next_load.write(data)
            prev_load.close()
            next_load.close()
            if doprint:
                printout('Iteration %d did not need lambda correction.', it_num)
    
    # ### Retrieve 'next' interation values
    if fin_iter2:
        input_new = fin_iter2
    else:
        infile = datadir + '/lagrange-iteration-' + str(it_num) + '.txt'
        input_new = form.readoutput(infile)
    
    x_new = input_new[4]
    x_bar_new = input_new[7]
    # ### Calculate difference to see if it matches precision
    diff = abs(x_old - x_new)
    #print(diff)
    unsatisfied = [d for d in diff if d > precision]
    
    
    # ### Check if precision is met, repeat if not
    if size(unsatisfied) == 0: # Precision is met
        printout('Precision of ' + str(precision) + ' is satisfied.\n')
        repeat = False
        delta = x_new - x
        delta_bar = x_bar_new - x_bar
        form.output_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, doprint)
        form.fancyout_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, pressure, temp, doprint)
        form.cleanup(datadir, it_num+1, clean)

    elif it_num < maxiter: # Precision is not met, max iteration not met
        it_num += 1
        x_old = x_new
        x_bar_old = x_bar_new
        input_old = input_new
        if doprint:
            printout('Precision not met. Starting next iteration...\n')
    
    # ### Stop if iteration 100 is reached (consider that 'good')
    elif it_num >= maxiter:
        printout('Maximum iteration reached, ending minimization.\n')
        repeat = False
        delta = x_new - x
        delta_bar = x_bar_new - x_bar
        form.output_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, doprint)
        form.fancyout_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, pressure, temp, doprint)
        form.cleanup(datadir, it_num+1, clean)

while (repeat & (not fullout)):
    printout("Testing!")
    repeat = False
