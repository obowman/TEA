#! /usr/bin/env python

# runatm.py
# ################
# In-shell inputs: file that contains atm data, one-word-description
#         Example:
#                  runatm.py inputs/atm_dummy ExampleAtm.dat
#
# ################
# Single-use function to run TEA over a standard atmosphere file containing atomic abundances
# Specifically, this should be used for multiple-line abundances/temps/pressures
#
# In order, this runs...
#     makeheader.py
#     balance.py
#     iteraten.py
#
# ###### FUNCTION TODO:
#    X : Accept appropriate parameters
#      : Negate need for writing files at all before end
#    X : Complete multi-run program!

''' # FOR TESTING
runatm.py inputs/atm_dummy.dat TimesTest 2>&1 | tee runtimes.txt 
'''

from TEA_config import *

# Setup for time/speed testing
if times:
    import time
    start = time.time()

import os
import shutil
import subprocess
import numpy         as np
import format        as form
import readatm       as ra
import makeatmheader as mah
from multiprocessing import Process, Queue
from sys import argv

# Time / speed testing
if times:
    end = time.time()
    elapsed = end - start
    print("runatm.py imports:  " + str(elapsed))

# Retrieve atm file
infile  = argv[1:][0]# + '.dat'
desc    = argv[1:][1]

# Set up locations of necessary scripts and directories of files
cwd = os.getcwd() + '/'
loc_readatm    = cwd + "readatm.py"
loc_makeheader = cwd + "makeheader.py"
loc_balance    = cwd + "balance.py"
loc_iterate    = cwd + "iterate.py"
loc_headerfile = cwd + "/headers/header_" + desc + ".txt"
loc_outputs    = cwd + "/outputs/" + desc + "/"
out_dir        = cwd + "/results/" + desc + "/"
single_res     = ["results-machine-read.txt", "results-visual.txt"]

# Read pre-atm file
n_runs, spec_list, radi_arr, pres_arr, temp_arr, atom_arr, end_head = ra.readatm(infile)

# Write output atm file once, keep open to add new lines
if not os.path.exists(out_dir): os.makedirs(out_dir)
fout_name = out_dir + desc + '.dat'
fout = open(fout_name, 'w+')

# Get header from pre-atm file
fin  = open(infile, 'r+')
inlines = fin.readlines()
fin.close()

# Write non-TEA atm info and first line of table (labels)
for i in np.arange(end_head):
    fout.writelines([l for l in inlines[i]])
    
fout.write(radi_arr[0].rjust(10) + ' ')
fout.write(pres_arr[0].rjust(10) + ' ')
fout.write(temp_arr[0].rjust(7) + ' ')
for i in np.arange(np.size(spec_list)):
    fout.write(spec_list[i].rjust(10)+' ')
fout.write('\n')

# Time / speed testing
if times:
    new = time.time()
    elapsed = new - end
    print("pre-science:        " + str(elapsed))

# Detect operating system for multi-processor support
if os.name == 'nt': inshell = True    # Windows
else:               inshell = False   # OSx / Linux

# Loop over all lines in pre-atm file and execute TEA loop
for q in np.arange(n_runs)[1:]:
    if doprint:
        print("\nReading atm file, TP line " + str(q))
    else:
        print('\n'+ str(q))
    
    # Radius, pressure, and temp for that line    
    radi = radi_arr[q]
    pres = pres_arr[q]
    temp = temp_arr[q]
    
    # Produce header for single lien of file, run balace and iterate
    mah.makeatmheader(q, spec_list, \
                              pres_arr, temp_arr, atom_arr, desc)
    
    # Time / speed testing for balance
    if times:
        ini = time.time()
    
    # Get balanced initial guess for this line
    if testbool:
        print("Guess Testing")
        if q > 1:
            #print(desc)
            #print(q)
            #print(out_dir + single_res[0])
            #print(out_dir + "Previous_Result.txt")
            #print(loc_outputs + "lagrange-iteration-0.txt")
            if not os.path.exists(loc_outputs): os.makedirs(loc_outputs)
            shutil.copy(out_dir + "Previous_Result.txt", loc_outputs + "lagrange-iteration-0.txt")
        else:
            subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)], shell = inshell)
    else:
        subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)], shell = inshell)
        
    if times:
        fin = time.time()
        elapsed = fin - ini
        print("balance.py:         " + str(elapsed))
    
    # Execute main TEA loop for this line
    subprocess.call([loc_iterate, loc_headerfile, desc, str(doprint)], shell = inshell)
    
    # Read output of TEA loop
    header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar = form.readoutput('results/' + desc + '/results-machine-read.txt')
    
    
    # Insert data from this line's results to atm file
    fout.write(radi.rjust(10) + ' ')
    fout.write(pres.rjust(10) + ' ')
    fout.write(temp.rjust(7) + ' ')
    for i in np.arange(np.size(spec_list)):
        cur_abn = x[i] / x_bar
        fout.write('%1.4e'%cur_abn + ' ')
    
    fout.write('\n')
    
    if testbool:
        shutil.copy(out_dir + single_res[0], out_dir + "Previous_Result.txt")
    
    
    # ### Perserve or delete intermediate files
    # Save / remove headers
    if save_headers:
        old_name = loc_headerfile
        new_name = loc_headerfile[0:-4] + "_" + '%.0f'%float(temp) + "K" + loc_headerfile[-4::]
        if os.path.isfile(new_name):
            os.remove(new_name)
        os.rename(old_name, new_name)
    else:
        old_name = loc_headerfile
        os.remove(old_name)
    
    # Save / remove lagrange.py / lambdacorr.py outputs
    if save_outputs:
        # Intermediate files
        old_name = loc_outputs
        new_name = loc_outputs[0:-1] + "_" + '%.0f'%float(temp) + "K" + loc_outputs[-1::]
        if os.path.exists(new_name):
            for file in os.listdir(new_name):
                os.remove(new_name + file)
            os.rmdir(new_name)
        os.rename(old_name, new_name)
        # Single-TP result files
        single_dir =  out_dir + "singles_" + '%.0f'%float(temp) + "K" + "/"
        if not os.path.exists(single_dir): os.makedirs(single_dir)
        for file in single_res:
            if os.path.isfile(single_dir + file):
                os.remove(single_dir + file)
            os.rename(out_dir + file, single_dir + file) 
    else:
        # Intermediate files
        old_name = loc_outputs
        for file in os.listdir(old_name):
            os.remove(old_name + file)
        os.rmdir(old_name)
        # Single-TP result files
        for file in single_res:
            os.remove(out_dir + file)

fout.close()

# End of file
