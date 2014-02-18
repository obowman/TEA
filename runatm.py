#! /usr/bin/env python

# In-shell inputs: file that contains atm data, one-word-description, True/False printing
#
# EXAMPLE:
'''
runatm.py inputs/atm_dummy ExampleAtm.dat False
'''
# NOTE: stoch.txt and gdata must already exist.

# runatm.py
# ############
# Single-use function to run TEA over a standard atmosphere file containing atomic abundances
# Specifically, this should be used for multiple-line abundances/temps/pressures
#
# In order, this runs...
#     makeheader.py
#     balance.py
#     iteraten.py
#
# Will fill this in better later, but that's the bones of it!

# ###### FUNCTION TODO:
#    X : Accept appropriate parameters
#      : Negate need for writing files at all before end
#    X : Complete multi-run program!

import os
import re
import sys
import subprocess
import numpy         as np
import format        as form
import readatm       as ra
import makeatmheader as mah
from multiprocessing import Process, Queue
from sys import argv
from ast import literal_eval

# ### Retrieve atm file
infile  = argv[1:][0]# + '.dat'
desc    = argv[1:][1]
doprint = literal_eval(argv[1:][2])

# Set up locations of necessary scripts and directories as well as bools and files
save_headers = False
save_outputs = False # NOTE: Must also have 'clean', 'nofile' as False in iterate.py
cwd = os.getcwd() + '/'
loc_readatm    = cwd + "readatm.py"
loc_makeheader = cwd + "makeheader.py"
loc_balance    = cwd + "balance.py"
loc_iterate    = cwd + "iterate.py"
loc_headerfile = cwd + "/headers/header_" + desc + ".txt"
loc_outputs    = cwd + "/outputs/" + desc + "/"
out_dir        = cwd + "/results/" + desc + "/"
single_res     = ["results-machine-read.txt", "results-visual.txt"]

n_runs, spec_list, radi_arr, pres_arr, temp_arr, atom_arr, end_head = ra.readatm(infile)

# ######################### EVENTUALY LOOP THIS OVER n_runs!
# WRITE OUTPUT ATM FILE ONCE, keep open to add new lines!
if not os.path.exists(out_dir): os.makedirs(out_dir)
fout_name = out_dir + desc + '.dat'

# Get header from pre-atm file
fin  = open(infile, 'r+')
inlines = fin.readlines()
fin.close()

# Write non-TEA atm info and first line of table (labels)
fout = open(fout_name, 'w+')

for i in np.arange(end_head):
    fout.writelines([l for l in inlines[i]])
    
fout.write(radi_arr[0].rjust(10) + ' ')
fout.write(pres_arr[0].rjust(10) + ' ')
fout.write(temp_arr[0].rjust(7) + ' ')
for i in np.arange(np.size(spec_list)):
    fout.write(spec_list[i].rjust(10)+' ')
fout.write('\n')


# start at 1, since first value is identifier
for q in np.arange(n_runs)[1:]:
    if doprint:
        print("\nReading atm file, TP line " + str(q))
    else:
        print('\n'+ str(q))
    radi = radi_arr[q]
    pres = pres_arr[q]
    temp = temp_arr[q]
    
    # Produce header for single lien of file, run balace and iterate
    mah.makeatmheader(q, spec_list, \
                              pres_arr, temp_arr, atom_arr, desc)
    #print(loc_balance, loc_iterate)
    subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)], shell=True)
    subprocess.call([loc_iterate, loc_headerfile, desc, str(doprint)], shell=True)
    
    header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar = form.readoutput('results/' + desc + '/results-machine-read.txt')
    
    fout.write(radi.rjust(10) + ' ')
    fout.write(pres.rjust(10) + ' ')
    fout.write(temp.rjust(7) + ' ')
    for i in np.arange(np.size(spec_list)):
        cur_abn = x[i] / x_bar
        fout.write('%1.4e'%cur_abn + ' ')
    
    fout.write('\n')
    
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