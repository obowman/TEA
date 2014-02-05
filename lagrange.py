# LAGRANGE.PY
# Executed by iterate.py

#print('Lagrange imports...')
import numpy as np
from sys import argv
from sympy.core import Symbol
from sympy.solvers import solve
import os
os.environ['OMP_NUM_THREADS']='10'
import format as form


def lagrange(it_num, datadir, doprint, direct=False, fromatm=False, dex=False):
    '''
    DESC HERE
    
    'b' it accepts is ABUNDANCE, want COUNT
    '''
    
    infile = datadir + '/lagrange-iteration-' + np.str(it_num - 1) + '.txt'
    
    # ### Read in values from header.txt and previous output
    if direct:
        input = direct
    else:
        input = form.readoutput(infile)
    
    header = input[0]
    pressure, temp, i, j, speclist, a, b, c = form.readheader(header, fromatm, dex)
    
    y     = input[4] # 'x' in output file, using final values as new initials
    y_bar = input[7] # see above
    
    # Convert b to counts
    # FINDME TOTAL
    #b *= 10
    #print(b)
    
    # ### Perform checks to be safe
    it_num_check = input[1]
    speclist_check = input[2]
    
    check = np.array([
            it_num_check != it_num - 1,
            False in (speclist_check == speclist) ])
    
    if check[0]:
        print("\n\nMAJOR ERROR! Read in file's it_num is not the most previous iteration!\n\n")
    
    if check[1]:
        print("\n\nMAJOR ERROR! Read in file uses different species order/list!\n\n")
    
    save_JANAF = False
    if save_JANAF:
        dir_save = os.getcwd()
        # CHANGE THIS TO MATCH DESC IN runatm.py or runinput.py
        desc_save = 'checkJANAF'
        JANAF_file_save = '/outputs/' + desc_save + '/JANAF_check_' + '%.0f'%temp + 'K.txt' 
        f = open(dir_save + JANAF_file_save, 'w+')
        for r in np.arange(np.size(speclist)):
            f.write(speclist[r] + '  ' + '%4.3f'%c[r] + '\n')
            #print(speclist[r], c[r])
        f.close()
        
    
    # Correct 'c' value for pressure     
    c += np.log(pressure)
    
    # ### Set up values of fi(Y) over different values of i
    fi_y = np.zeros(i)
    
    for n in np.arange(i):
        y_frac  = np.float(y[n] / y_bar)
        fi_y[n] = y[n] * ( c[n] + np.log(y_frac) )
    
    # ### Set up values of rjk over different values of i
    # NOTE: j , k = 1, 2, ... , total elements 
    #       so rj_k = rk_j, making a matrix symmetrical across the diagonal
    k = j # Both the same size
    rjk = np.zeros((j,k))
    for l in np.arange(k):
        for m in np.arange(j):
            foo = 0.0
            for n in np.arange(i): # summate (ai_j * ai_k * yi) over i
                foo += a[n, m] * a[n, l] * y[n]
            rjk[m, l] = foo
    
    
    # ### Set up value of u
    # Depends on if you want output of u or output of xi
    # For now, use u for simplicity in checking
    #u = -1. + (x_bar/y_bar)
    u = Symbol('u')
    
    
    # ### Set up pi_j variables, where j is species index
    # Example: pi_2 is lagrangian multipier of N (j = 2)
    pi = []
    for m in np.arange(j):
        name = 'pi_' + np.str(m+1)
        pi = np.append(pi, Symbol(name))
    
    
    # ### Set up r_jk * pi_j summations
    # There will be j x k terms of r_jk * pi_j
    sq_pi = [pi]
    for m in np.arange(j-1):
        sq_pi = np.append(sq_pi, [pi], axis = 0) # Make square array of pi values with shape j x k
    
    rpi = rjk * sq_pi # Multiply rjk * sq_pi to get array of rjk * pi_j 
    
    
    # ################################################################### #
    # ####################### SET FINAL EQUATIONS! ###################### #
    # ################################################################### #
    # Total number of equations is j + 1
    
    # ### Set up ai_j * fi(Y) summations
    aij_fiy = np.zeros((j))
    for m in np.arange(j):
        foo = 0.0
        for n in np.arange(i): # summate (ai_j * fi(Y)) over i
            foo += a[n,m] * fi_y[n]
        aij_fiy[m] = foo
    
    # ### Create first j-1 equations
    for m in np.arange(j):
        if m == 0:
            equations   = np.array([np.sum(rpi[m]) + b[m]*u - aij_fiy[m]])
        else:
            lagrange_eq = np.array([np.sum(rpi[m]) + b[m]*u - aij_fiy[m]])
            equations   = np.append(equations, lagrange_eq)
    
    
    # ### Last equation, only one here
    bpi = b * pi
    lagrange_eq = np.array([np.sum(bpi) - np.sum(fi_y)])
    equations = np.append(equations, lagrange_eq)
            
    # ### Solve final system of equations
    unknowns = list(pi)
    unknowns.append(u)
    fsol = solve(list(equations), unknowns)
    
    
    # ################################################################### #
    # ########################## GET xi VALUES ########################## #
    # ################################################################### #
    
    pi_f = []
    for m in np.arange(j):
        pi_f = np.append(pi_f, [fsol[pi[m]]])
    
    u_f = fsol[u]
    x_bar = (u_f + 1.)*y_bar
    
    # Start array for x values size of i
    x = np.zeros(i)
    
    # Apply Lagrange solution for final values (eq 14)
    for n in np.arange(i):
        sum_pi_aij = 0.0
        for m in np.arange(j):
            sum_pi_aij += pi_f[m] * a[n, m]
        x[n] = - fi_y[n] + (y[n]/y_bar) * x_bar \
             + sum_pi_aij * y[n]
    
    
    # ### Now have final mole values for this iteration!         
    # Also note the distance between initial and final
    # Correct x_bar
    x_bar = np.sum(x)
    delta = x - y
    delta_bar = x_bar - y_bar
    
    # ### Export all values into output files
    #if doprint:
    #print(np.sum(x))
    #print(x_bar)
    
    if direct:
        return [header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar]
    else:
        form.output_nocorr(datadir, header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint)
        form.fancyout_nocorr(datadir, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint)
        return False
        
