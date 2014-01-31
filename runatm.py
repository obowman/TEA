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
#      : Accept appropriate parameters
#      : Negate need for writing files at all before end
#      : Complete multi-run program!

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

# Set up locations of necessary scripts
cwd = os.getcwd() + '/'
loc_readatm    = cwd + "readatm.py"
loc_makeheader = cwd + "makeheader.py"
loc_balance    = cwd + "balance.py"
loc_iterate    = cwd + "iterate.py"
loc_headerfile = cwd + "/headers/header_" + desc + ".txt"

n_runs, spec_list, radi_arr, pres_arr, temp_arr, atom_arr, end_head = ra.readatm(infile)

# ######################### EVENTUALY LOOP THIS OVER n_runs!
# WRITE OUTPUT ATM FILE ONCE, keep open to add new lines!
out_dir = 'results/' + desc + '/'
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
    #print(q, spec_list, \
    #                           pres_arr, temp_arr, atom_arr, desc)
    #p1 = Process(target = mah.makeatmheader, args=(q, spec_list, \
    #                           pres_arr, temp_arr, atom_arr, desc))
    
    #p1.start()
    #p1.join() 
        

    #p2 = Process(target = subprocess.call, args = [loc_balance, loc_headerfile, desc, str(doprint)])
    #p3 = Process(target = subprocess.call, args = [loc_iterate, loc_headerfile, desc, str(doprint)])
    
    mah.makeatmheader(q, spec_list, \
                              pres_arr, temp_arr, atom_arr, desc)
    subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)])
    subprocess.call([loc_iterate, loc_headerfile, desc, str(doprint)])
     
    #p2.start()
    #p2.join()
    #p3.start()
    #p3.join()
    
    header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar = form.readoutput('results/' + desc + '/results-machine-read.txt')
    
    fout.write(radi.rjust(10) + ' ')
    fout.write(pres.rjust(10) + ' ')
    fout.write(temp.rjust(7) + ' ')
    for i in np.arange(np.size(spec_list)):
        cur_abn = x[i] / x_bar
        fout.write('%1.4e'%cur_abn + ' ')
    
    fout.write('\n')


fout.close()

