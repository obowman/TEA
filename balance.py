#! /usr/bin/env python

# balance.py
# ################
# In-shell inputs: header file, name of data directory
#         Example:
#                  balance.py full_White2.txt testing2
#
# ################
# DOCSTRING HERE

from TEA_config import *

import os
import numpy as np
from sys import argv
from ast import literal_eval
from sympy.core    import Symbol
from sympy.solvers import solve

import format as form

# Read from shell input and create data directory
header  = argv[1:][0]
datadir = 'outputs/' + argv[1:][1]
if not os.path.exists(datadir): os.makedirs(datadir)

# Read in values from header file
pressure, temp, i, j, speclist, a, b, c = form.readheader(header, dex)

if doprint:
    print("b values: " + str(b))

# ### Set initial values of all but 'j' y_initial values to 'scale' moles
#     This actual number is arbitrary; after iterations, solution will converge regardless 
#     of the input used.  This just establishes a valid input.
#     'j' y_initials will be free and solved by this program.
# NOTE: ai_j values for the three free variables cannot all be 0 for any given j.

# Find chunk of ai_j that will allow the corresponding yi values to be free variables
for n in np.arange(i - j + 1):
    # Get lower and upper indicies for chunk of ai_j to check
    lower = n
    upper = n + j
    
    # Retrieve chunk of ai_j that would contain free varaibles
    a_chunk = a[lower:upper]
    
    # Sum columns to get total of a in chunk for each species 'j' and feed into check
    check = map(sum,zip(*a_chunk))
    
    # Look for 0's in check
    # If 0 is found, this chunk of a can't be used for free variables
    has_zero = 0 in check
    
    if has_zero == False:
        free_id = []
        # Create list of free variables indicies
        for m in np.arange(j):
            if doprint == True:
                print('Using y_' + np.str(n + m + 1) + ' as a free variable')
            free_id = np.append(free_id, n + m)
        break


# Seek proper inputs to allow only positive initial values
scale = 1e-1
nofit = True

while nofit:
    # Set up list of 'known' initial values before and after free chunk
    pre_free = np.zeros(free_id[0]) + scale
    post_free = np.zeros(i - free_id[-1] - 1) + scale
    
    # Set up list of free variables
    free = []
    for m in np.arange(j):
        name = 'y_unknown_' + np.str(m)
        free = np.append(free, Symbol(name))
        #print(solve(free[m], free[m]))

    # Combine free and known to make array of y_initial values
    y_init = np.append(pre_free,      free)
    y_init = np.append(  y_init, post_free)

    # Make 'j' equations satifying mass balance:
    # sum_i(ai_j * y_i) = b_j
    eq = [[]]
    for m in np.arange(j):
        foo = 0
        for n in np.arange(i):
            foo += a[n, m] * y_init[n]
        rhs = -b[m] + foo
        eq = np.append(eq, rhs)
        
    # Solve system of linear equations to get the values of the yi's that were free
    #print(list(eq))
    result = solve(list(eq), list(free))
    
    # Correct for no-solution-found results. If found, decrease scale size.
    if result == []:
        scale /= 10
        if doprint:
            print("Correcting initial guesses for realistic mass. Trying " + str(scale) + "...")
    
    # Correct for negative-mass results.  If found, decrease scale size.
    else:
        hasneg = False    
        for m in np.arange(j):
            if result[free[m]] < 0: hasneg = True
        
        if hasneg:

            scale /= 10
            if doprint:
                print("Negative numbers found in fit.")
                print("Correcting initial guesses for realistic mass. Trying " + str(scale) + "...")
        else:
            nofit = False
            if doprint:
                print(str(scale) + " provided a viable initial guess.")
    

# Put these new values into the final y_init array
fit = []
for m in np.arange(j):
    fit = np.append(fit, result[free[m]])

y_init[free_id[0]:free_id[j-1]+1] = fit


# ### CHECKS ### #
if doprint == True:
    print('\nCHECKS:')

for m in np.arange(j):
    # NOTE! Round accounts for float vs int boolean, NOT ACTUALLY CHANGING ANY VALUES!
    bool = round((sum(a[:,m] * y_init[:])), 2) == round(b[m], 2)
    if bool == True:
        if doprint == True:
            print('Equation ' + np.str(m+1) + ' is satisfied.')
    if bool == False:
        print('Equation ' + np.str(m+1) + ' is NOT satisfied. Check for errors!')


# Put results into machine-readable file
it_num    = 0
y         = y_init
y_bar     = np.sum(y)
delta     = np.zeros(i)   # For pipeline readability
delta_bar = np.sum(delta) # For pipeline readability

form.output(datadir, header, it_num, speclist, y, y, delta, y_bar, y_bar, delta_bar, False)
form.fancyout(datadir, it_num, speclist, y, y, delta, y_bar, y_bar, delta_bar, False)

# End of file