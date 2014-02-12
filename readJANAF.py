#! /usr/bin/env python

# READJANAF.PY
# In-shell inputs: True/False reading/writing printout

# ####################################################################### #
# ##################### CHANGE THESE VARIABLES ONLY ##################### #
# ####################################################################### #
# Directory name of raw JANAF tables
raw_dir = 'rawtables'

# Direcoty name of output, TEA-read files
out_dir = 'gdata'

# #################### END OF USER DEFINED VARIABLES #################### #

import numpy as np
from ast import literal_eval
from sys import argv
import re
import os
import string
from comp import comp

# False or True for printing errors, delete old version of stochdir if True
doprint = literal_eval(argv[1:][0])

# Correct directory names
if raw_dir[-1] != '/':
    raw_dir += '/'

if out_dir[-1] != '/':
    out_dir += '/'
    
# Get number of elements used
n_ele = np.shape(comp(''))[0]

# H-065.txt is l,g water 1bar
# Get all JANAF file names and make empty array for specie data extraction
JANAF_files = os.listdir(raw_dir)
n_JANAF = np.size(JANAF_files)
species = np.empty((n_JANAF, 4), dtype='|S50')

# Loop over all JANAF files to get specie names
for i in np.arange(n_JANAF):
    infile = raw_dir + JANAF_files[i]
    f = open(infile, 'r')
    line = [value for value in f.readline().split()]
    f.close()
    string = ' '.join(line)
    # Get the specie name from the JANAF file
    specie = re.search(' \((.*?)\) ', string).group(1)
    # Correct name for ions
    start = string.find(' (' + specie)
    if specie[-1] == '+':
        specie = specie.strip('+') + '_ion_p'
    if specie[-1] == '-':
        specie = specie.strip('-') + '_ion_n'
    
    species[i, 0] = specie
    
    
    # add correction for doubles
    doubles = string[: start].split()
    add_string = doubles[-1]
    #print 'jasmina printa add_string', add_string, line
    species[i, 3] = add_string

    
    
# Loop over all JANAF files to get species stochiometric coefficients
for i in np.arange(n_JANAF):
    infile = raw_dir + JANAF_files[i]
    f = open(infile, 'r')
    line = [value for value in f.readline().split()]
    f.close()
    string = ' '.join(line)
    state = re.search('\((.*?)\)', line[-1]).group(0)
    stoch = line[-1].strip(state)
    outstate = re.search('\((.*?)\)', state).group(1).replace(',', '-')
    stoch = stoch.strip('+')
    stoch = stoch.strip('-')
    species[i, 1] = stoch
    species[i, 2] = outstate

# Establish header used for JANAF tables
header = ['T (K)', '-[G-H(Tr)]/T (J/K/mol)', 'delta-f H (kJ/mol)']
 
# Set file containing list of JANAFs converted
file_list = open('conversion_record.txt', 'w+')

# Setup for general loop and redunancy checks
ID_originals = {}
is_redundant = {} 
print_label  = True
n_files = 0

# Check for redundancies, only insert additional label if more than one
#  species with same formula is in data
for i in np.arange(n_JANAF):
    infile = raw_dir + JANAF_files[i]
    outfile = out_dir + species[i, 0] + '_' + np.str(species[i,2]) + '.txt'
    if ID_originals.has_key(outfile):
        is_redundant[outfile] = infile
    else:
        ID_originals[outfile] = infile
    
# Loop over all JANAF tables and convert to TEA-read
for i in np.arange(n_JANAF):
    # Read in current JANAF table
    infile = raw_dir + JANAF_files[i]
    f = open(infile, 'r')
    
    # Read in data from JANAF table
    data = []
    getpressure = True
    for line in f.readlines():
        l = [value for value in line.split()]
        if getpressure:
            pressline = ' '.join(l) # Save line with pressure for later use
            getpressure = False 
        haschar = re.findall('[A-z]', ' '.join(l))
        hasnum = re.findall('[0-9]', ' '.join(l))
        length = np.size(l)
        if (haschar == [] and length >= 8 and hasnum != []):
            # Will not read lines with comments or with missing data
            data.append(l)
    f.close()
    
    # Get pressure of JANAF table
    if re.search(', (.*?) Bar \(', pressline):
        # Removes ' Bar' from the pressure string
        pressure = np.int(re.search(', (.*?) Bar \(', pressline).group(1))
    else:
        pressure = 1 # If pressure isn't listed, JANAF table assumes 1 bar
    
    # Put data into array with correct data types and header
    n_temps = np.shape(data)[0]
    gdata = np.empty((n_temps, 3), dtype='|S50')
    for j in np.arange(n_temps):
        gdata[j,0] = data[j][0]
        gdata[j,1] = data[j][3]
        gdata[j,2] = data[j][5]
    
    # Create directory for converted files
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    # Create file for specific JANAF specie, adding addition comment if redundant
    if pressure == 1: # For constency, only use 1bar tables (only H2O has other pressures)
        outfile = out_dir + species[i, 0] + '_' + np.str(species[i,2]) + '.txt'
        
        if is_redundant.has_key(outfile):
            outfile = out_dir + species[i, 0] + '_' + np.str(species[i,2]) + '_' + np.str(species[i,3]) + '.txt'
        
        if doprint:
            print(outfile.split('.')[0])
        file_list.write(outfile+'\n')
        f = open(outfile, 'w+')
        n_files += 1
        # Write data from JANAF table
        f.write(header[0].ljust(8))
        f.write(header[1].ljust(24))
        f.write(header[2].ljust(22))
        f.write('\n')
        for h in np.arange(n_temps):
            f.write(gdata[h, 0].ljust(8))
            f.write(gdata[h, 1].ljust(24))
            f.write(gdata[h, 2].ljust(22))
            f.write('\n')
        
        f.close()
    else:
        if print_label:
            print('These files were not included because pressure != 1bar:')
            print_label = False
        print('    ' + infile.split('/')[-1] + ' (' + species[i, 0] + '_' \
               + np.str(species[i,2]) + ')')

print("\nSaved " + str(n_files) + " TEA-read files to \'" + out_dir + "\', out of the available " \
      "\n      " + str(n_JANAF) + " JANAF files in the \'" + raw_dir + "\' directory.")
print("\nSaved list of converted files to \'conversion_record.txt.\'")
    
file_list.close()


