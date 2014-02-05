#! /usr/bin/env python

# READJANAF.PY
# In-shell inputs: True/False error printing

import numpy as np
from ast import literal_eval
from sys import argv
import re
import os
import string

# THIS IS JUST FOR OLIVER'S USE! DO NOT USE ON LINUX
#os.chdir('C:\\Users\\Nestor\\My Work\\ESP 01\\TEA')
# ENDS OLIVER-ONLY CODE
from comp import comp

# False or True for printing errors, delete old version of stochdir if True
errorprint = literal_eval(argv[1:][0])

# Get number of elements used
n_ele = np.shape(comp(''))[0]

# H-065.txt is l,g water 1bar
# Get all JANAF file names and make empty array for specie data extraction
JANAF_files = os.listdir('rawtables')
n_JANAF = np.size(JANAF_files)
species = np.empty((n_JANAF, 4), dtype='|S50')

# Loop over all JANAF files to get specie names
for i in np.arange(n_JANAF):
    infile = 'rawtables/' + JANAF_files[i]
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
    infile = 'rawtables/' + JANAF_files[i]
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

#for i in np.arange(n_JANAF):
#    species[i, 0].replace('.', '-')


# ### INCOMPLETE PAST HERE ###

# Establish header used for JANAF tables
header = ['T (K)', '-[G-H(Tr)]/T (J/K/mol)', 'delta-f H (kJ/mol)']



ID_originals = {}   


file_list = open('jass_files.txt', 'w+')
# to sort do this:
# sort jass_files.txt >jass_sort.txt

#print n_JANAF
n_files = 0
# Loop over all JANAF tables
for i in np.arange(n_JANAF):
    # Read in current JANAF table
    infile = 'rawtables/' + JANAF_files[i]
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
    
    # Create directory for gdata files
    gdir = 'gdata/'
    if not os.path.exists(gdir): os.makedirs(gdir)
    
    # Create file for specific JANAF specie
    if pressure == 1: # For constency, only use 1bar tables (only H2O has other pressures)
        outfile = gdir + species[i, 0] + '_' + np.str(species[i,2]) + '.txt'

        if ID_originals.has_key(outfile):
             print ID_originals[outfile], infile, outfile
             outfile = gdir + species[i, 0] + '_' + np.str(species[i,2]) + '_' + np.str(species[i,3]) + '.txt'
             

        else:
             ID_originals[outfile] = infile


        file_list.write(outfile+'\n')
        f = open(outfile, 'w+')
        n_files = n_files + 1
        # Read in data from JANAF table
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
        print 'this file is not included because pressure != 1bar ==>', infile

file_list.close()




