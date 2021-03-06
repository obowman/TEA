#! /usr/bin/env python

# runsingle.py
# ################
# In-shell inputs: file that contains user inputs, one-word-description, True/False printing
#         Example:
#                  runinput.py inputs/input_White ExampleRun.txt
#
# ###############
# Single-use function to run TEA over a standard inputs file
# Specifically, this should be used for single-input abundances/temps/pressures
#
# In order, this runs...
#     makeheader.py
#     balance.py
#     iteraten.py
#
# ###### FUNCTION TODO:
#    X : Accept appropriate parameters
#      : Negate need for writing files at all before end
#    X : Complete single-run program!

from TEA_config import *

import os
import numpy as np
import subprocess
import format as form
from sys import argv
    
# Retrieve user inputs file
infile  = argv[1:][0]# + '.txt'
desc    = argv[1:][1]

# Set up locations of necessary scripts and directories of files
cwd = os.getcwd() + '/'
loc_makeheader = cwd + "makeheader.py"
loc_balance    = cwd + "balance.py"
loc_iterate    = cwd + "iterate.py"
loc_headerfile = cwd + "/headers/header_" + desc + ".txt"

subprocess.call([loc_makeheader, infile, desc, str(doprint)])
subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)])
subprocess.call([loc_iterate, loc_headerfile, desc, str(doprint)])

# End of file