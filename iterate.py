#! /usr/bin/env python

# iterate.py
# ################
# In-shell inputs: header file, name of data directory
#         Example:
#                  iterate.py full_White2.txt testing2
#
# ################
# DOCSTRING HERE

from TEA_config import *

# Setup for time/speed testing
if times:
    import time
    start = time.time()

from numpy import size
from numpy import where
from multiprocessing import Process, Queue
from sys import argv
from sys import stdout

import lagrange   as lg
import lambdacorr as lc
import format     as form
from   format import printout

# Time / speed testing
if times:
    end = time.time()
    elapsed = end - start
    print("iterate.py imports: " + str(elapsed))

# Read run-time arguments
header   = argv[1:][0] # name of header file
datadir  = 'outputs/' + argv[1:][1] # location of storage directory
datadirr = 'results/' + argv[1:][1] # location of final results

# Retrieve and set header info
inhead   = form.readheader(header)
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


# Setup up first iteration (always has to be at least 1 iteration)
it_num  = 1
repeat  = True

# Prepare iterative process to accept either files or pass data in memory
fin_iter2 = [header, 0, speclist, x, x, 0, x_bar, x_bar, 0]


# Time / speed testing
if times:
    new = time.time()
    elapsed = new - end
    print("pre-loop setup:     " + str(elapsed))

# ### Perform main TEA loop, repeating lagrange minimization and lambda correction 
#    for as long as is necessary given max iterations, precision, etc.  Loop is
#    performed in chunks of two to allow comparison between two most recent loops
#    without isolting the first loop.
while repeat:
    # Simple progress info
    if ((not doprint) & (not times)):
        stdout.write(' ' + str(it_num) + '\r')
        stdout.flush()
        
    # ### Perform 'starting' iteration
    # Time / speed testing for first lagrange
    if times:
        ini = time.time()
    
    # Execute lagrange minimization
    ini_iter = lg.lagrange(it_num, datadir, doprint, fin_iter2)
    
    if times:
        fin = time.time()
        elapsed = fin - ini
        print("lagrange" + str(it_num).rjust(4) + " :      " + str(elapsed))
    
    # Cleanup files that are no longer needed
    #form.cleanup(datadir, it_num, clean)
    
    if doprint:
        printout('Iteration %d Lagrange complete. Starting lambda correction...', it_num)
    
    # Recieve files by memory or file
    #if fin_iter2:
    lag_dat, lag_dat2 = ini_iter[4], ini_iter[7]
    #else:
    #    temp_in = form.readoutput(datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt")
    #    lag_dat, lag_dat2 = temp_in[4], temp_in[7]
    
    # Check if lambda correction is needed (negative masses), and perform if needed
    if where((lag_dat < 0) == True)[0].size != 0:
        # Correction is needed
        if doprint:
            printout('Correction required. Initializing...')
            
        # Time / speed testing for first lambda correction
        if times:
            ini = time.time()
        
        # Execute lambda correction
        ini_iter2 = lc.lambdacorr(it_num, datadir, doprint, ini_iter)
        
        if times:
            fin = time.time()
            elapsed = fin - ini
            print("lambcorr" + str(it_num).rjust(4) + " :      " + str(elapsed))
        
        if doprint:
            printout('Iteration %d lambda correction complete. Checking precision...', it_num)
    else:
        # ### Correction is not needed
        # Pass previous lagrange results as inputs to next iteration via memory or file
        #if fin_iter2:
        ini_iter2 = ini_iter
        if doprint:
            printout('Iteration %d did not need lambda correction.', it_num)
        #else:
        #    prev = datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt"
        #    prev_load = open(prev)
        #    next = datadir + "/lagrange-iteration-" + str(it_num) + ".txt"
        #    next_load = open(next, 'w')
        #    data = prev_load.read()
        #    next_load.write(data)
        #    prev_load.close()
        #    next_load.close()
        #    if doprint:
        #        printout('Iteration %d did not need lambda correction.', it_num)
    
    # Perform next iteration
    it_num += 1
    
    # Simple progress info
    if ((not doprint) & (not times)):
        stdout.write(' ' + str(it_num) + '\r')
        stdout.flush()
    
    # Time / speed testing for second lambda correction
    if times:
        ini = time.time()
    
    # Execute lagrange minimization
    fin_iter = lg.lagrange(it_num, datadir, doprint, ini_iter2)
    
    if times:
        fin = time.time()
        elapsed = fin - ini
        print("lagrange" + str(it_num).rjust(4) + " :      " + str(elapsed))
    
    if doprint:
        printout('Iteration %d Lagrange complete. Starting lambda correction...', it_num)
    
    # Cleanup files that are no longer needed
    #form.cleanup(datadir, it_num, clean)
    
    # Recieve files by memory or file
    #if fin_iter2:
    lag_dat = fin_iter[4]
    #else:
    #    lag_dat = form.readoutput(datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt")[4]
    
    # Check if lambda correction is needed (negative masses), and perform if needed
    if where((lag_dat < 0) == True)[0].size != 0:
        # Correction is needed
        if doprint:
            printout('Correction required. Initializing...')
            
        # Time / speed testing for second lambda correction
        if times:
            ini = time.time()
        
        # Execute lambda correction
        fin_iter2 = lc.lambdacorr(it_num, datadir, doprint, fin_iter)
        
        if times:
            fin = time.time()
            elapsed = fin - ini
            print("lambcorr" + str(it_num).rjust(4) + " :      " + str(elapsed))
        
        if doprint:
            printout('Iteration %d lambda correction complete. Checking precision...', it_num)
        
    else:
        # ### Correction is not needed
        # Pass previous lagrange results as inputs to next iteration via memory or file
        #if fin_iter2:
        fin_iter2 = fin_iter
        if doprint:
            printout('Iteration %d did not need lambda correction.', it_num)
        #else:
        #    prev = datadir + "/lagrange-iteration-" + str(it_num) + "-nocorr.txt"
        #    prev_load = open(prev)
        #    next = datadir + "/lagrange-iteration-" + str(it_num) + ".txt"
        #    next_load = open(next, 'w')
        #    data = prev_load.read()
        #    next_load.write(data)
        #    prev_load.close()
        #    next_load.close()
        #    if doprint:
        #        printout('Iteration %d did not need lambda correction.', it_num)
    
    # Retrieve most recent interation values
    #if fin_iter2:
    input_new = fin_iter2
    #else:
    #    infile = datadir + '/lagrange-iteration-' + str(it_num) + '.txt'
    #    input_new = form.readoutput(infile)
    
    x_new     = input_new[4]
    x_bar_new = input_new[7]
    
    # Calculate difference between last two iterations to see if it matches precision
    diff = abs(x_old - x_new)
    unsatisfied = [d for d in diff if d > precision]
    
    # Check if precision is met, repeat if not and iteration cap is not forced to completion
    if ((size(unsatisfied) == 0) & (not forceiter)): 
        # Precision is met
        printout('Precision of ' + str(precision) + ' is satisfied.\n')
        repeat = False
        delta = x_new - x
        delta_bar = x_bar_new - x_bar
        form.output_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, doprint)
        form.fancyout_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, pressure, temp, doprint)
        #form.cleanup(datadir, it_num+1, clean)

    elif it_num < maxiter: 
        # Precision is not met, max iteration not met
        it_num += 1
        x_old = x_new
        x_bar_old = x_bar_new
        input_old = input_new
        if doprint:
            printout('Precision not met. Starting next iteration...\n')
    
    # Stop if max iteration is reached 
    elif it_num >= maxiter:
        printout('Maximum iteration reached, ending minimization.\n')
        repeat = False
        delta = x_new - x
        delta_bar = x_bar_new - x_bar
        form.output_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, doprint)
        form.fancyout_results(datadirr, header, it_num, speclist, x, x_new, delta, x_bar, x_bar_new, delta_bar, pressure, temp, doprint)
        #form.cleanup(datadir, it_num+1, clean)

# End of file
