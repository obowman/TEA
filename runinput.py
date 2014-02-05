#! /usr/bin/env python

#In-shell inputs: file that contains user inputs, one-word-description, True/False printing
#
# EXAMPLE:
'''
runinput.py inputs/input_White ExampleRun.txt False
'''
# NOTE: stoch.txt and gdata must already exist.

# runinput.py
# ############
# Single-use function to run TEA over a standard inputs file
# Specifically, this should be used for single-input abundances/temps/pressures
#
# In order, this runs...
#     makeheader.py
#     balance.py
#     iteraten.py
#
# Will fill this in better later, but that's the bones of it!

# ###### FUNCTION TODO:
# CHECK: Accept appropriate parameters
#      : Negate need for writing files at all before end
# CHECK: Complete single-run program!

import os
#os.environ['OMP_NUM_THREADS']='10'
import sys
import numpy as np
import subprocess
import format as form
from sys import argv
from ast import literal_eval

# ### Retrieve user inputs file
infile  = argv[1:][0]# + '.txt'
desc    = argv[1:][1]
doprint = literal_eval(argv[1:][2])

# Set up locations of necessary scripts
cwd = os.getcwd() + '/'
loc_makeheader = cwd + "makeheader.py"
loc_balance    = cwd + "balance.py"
loc_iterate    = cwd + "iterate.py"
loc_headerfile = cwd + "/headers/header_" + desc + ".txt"

subprocess.call([loc_makeheader, infile, desc, str(doprint)])
subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)])
subprocess.call([loc_iterate, loc_headerfile, desc, str(doprint)])

