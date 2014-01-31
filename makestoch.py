# MAKESTOCH.PY
# In-shell inputs: True/False error printing

import numpy as np
from ast import literal_eval
from sys import argv
import re
import os
# THIS IS JUST FOR OLIVER'S USE! DO NOT USE ON LINUX
os.chdir('C:\\Users\\Nestor\\My Documents\\GitHub\\TEA')
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
species = np.empty((n_JANAF, 3), dtype='|S50')

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

# Loop over all JANAF files to write new stoch file
# NOTE!!!!!! DOES NOT ACCOUNT FOR MULTIPLE JANAFS WITH IDENTICAL 
#            ELEMENTS BUT WITH ADDED COMMENTS! OR FRACTIONAL ABUNDANCES!
#            OR IONS!
# EX: P-002.txt - P-007.txt negates redunacies! 
#     So only P-007.txt (Phosphorus, Black) is taken!
# EX: O2.72W1 will give 0 O's and 1 W!
for i in np.arange(n_JANAF):
    elements = comp(species[i, 1])
    stochdir = 'stochcoeff/'
    if not os.path.exists(stochdir): os.makedirs(stochdir)
    outfile = stochdir + species[i, 0] + '_' + species[i,2] + '.txt'
    if errorprint:
        if os.path.exists(outfile):
            print('File overwritten at i=' + np.str(i))
        if np.sum(elements[:,2]) == 0:
            print('Species \'' + np.str(species[i,0]) +'\' has no elements! i=' + np.str(i))
    f = open(outfile, 'w+')
    numcols = np.shape(elements)[1]
    numele = np.shape(elements)[0]
    for j in np.arange(numele):
        for h in np.arange(numcols):
            f.write(np.str(elements[j, h]).ljust(4))
        f.write('\n')
    f.close()

# ### Create all-in-one stoch file with abundances and all species/elements
# Retrieve abundance info
abun = 'abundances.txt'
f = open(abun, 'r')
abundata = []
for line in f.readlines():
    l = [value for value in line.split()]
    abundata.append(l)

abundata = np.asarray(abundata)
f.close()

# Write stoch file
outfile = 'stoch.txt'
f = open(outfile, 'w+')
f.write('b'.ljust(12))
for i in np.arange(n_ele):
    element = elements[i, 1]
    index = np.where(abundata[:, 1] == element)[0]
    if not index:
        f.write('0.'.rjust(6))
    else:
        ind = index[0]
        f.write(abundata[ind,2].rjust(6))

f.write('\n')
f.write('Species'.ljust(12))
for i in np.arange(n_ele):
    f.write(elements[i, 1].rjust(6))

f.write('\n')

for j in np.arange(n_JANAF):
    specie = species[j, 0]
    elements = comp(species[j, 1])
    f.write(specie.ljust(12))
    for i in np.arange(n_ele):
        f.write(np.str(elements[i, 2]).rjust(6))
    
    f.write('\n')

f.close()