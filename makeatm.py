#! /usr/bin/env python

'''
Quick program to produce a dummy pre-atm file

Quick assumptions:
 - solar abundances at all pressures
 - Dummy TP profile params (10 total)
 - Dummy pressures ,temps too
 - Dummy fillers
 - FINDTEA for TEA's sake
 - MANUALLY INPUT: ALLOWED SPECIES
 '''

import numpy as np

# ### User inputs ### #

filename    = 'Example.dat'   # Output atm file name

# Names for input elements must be simple atomic labels, and names for
#  output species must match those produced by readJANAF.py
in_elem     = "C H O N"        # Atomic label for input abundances
out_spec    = "H_g C_g N_g O_g H2_ref CO_g CH4_g H2O_g N2_ref NH3_g"   
                               # List of output species 
               
steps       = 100               # Number of steps in radius, pressure, and temperature               
rad         = np.linspace( 1e4,    1, steps)
pres        = np.logspace(  -5,    0, steps)
temp        = np.linspace( 100, 3000, steps)

# Optional data insertions
TP_params   = "# T-P profile parameters can go here."  # Dummy TP profile params
fillers     = "# ANY FILLER  \n\
# DATA CAN    \n\
# BE INJECTED \n\
# IN THIS AREA"  # Filler to save space
               
abun        = 'abundances.txt' # Input abundances (solar for this case)
header      = "\'\'\'                               \n\
This is a TEA pre-atmosphere input file.             \n\
                                                     \n\
TEA accepts a file in this format to produce molar   \n\
abundances as a function of pressure and temperature.\n\
Any non-TEA data may be added anywhere in the file   \n\
preceding the \"#FINDTEA\" marker.                  \n\
                                                     \n\
Output species must be added in the line immediately \n\
following the \"#FINDSPEC\" marker and must be named \n\
to match those produced by readJANAF.py.             \n\
\'\'\'"

solids      = False # FINDME: Correction for H2O condensation

# read abundance data
f = open(abun, 'r')
abundata = []
for line in f.readlines():
    l = [value for value in line.split()]
    abundata.append(l)

abundata = np.asarray(abundata)
f.close()

# Trim abundata to the stuff we care about
in_elem   = in_elem.split(" ")
nspec  = np.size(in_elem)
lookat = np.zeros(abundata.shape[0], dtype=bool)

for i in np.arange(nspec):
    lookat += (abundata[:,1] == in_elem[i])

abun_trim = abundata[lookat]

# Also read Si abundance (For Burrows Sharp 1999 quick fix)
Si_abun = (abundata[:,1] == 'Si')

# Create array that will be in output atm file...
out_elem = abun_trim[:,1].tolist()
out_dex  = abun_trim[:,2].tolist()
print(out_dex)
out_dex  = map(float, abun_trim[:,2])
out_num  = 10**np.array(out_dex)
out_abn  = (out_num / np.sum(out_num)).tolist()

# Implimenting solid quick fix Burrows Sharp 1999
Si_frac = 10**Si_abun[0] / np.sum(out_num)

for n in np.arange(np.size(out_abn)):
    out_abn[n] = str('%1.10e'%out_abn[n])


out = [['    Radius'] + ['Pressure'] + ['Temp'] + out_elem]




for i in np.arange(steps):
    # 'if' loop added for O solids
    if ((temp[i] < 1700) & solids):
        new = (float(out_abn[2]) - 3.28*Si_frac)
        out_abn[2] = str('%1.10e'%new)
        out.append(['%8.3f'%rad[i]] + ['%8.4e'%pres[i]] + ['%7.2f'%temp[i]] + out_abn)
    else:
        old = out_num[2] / np.sum(out_num) 
        out_abn[2] = str('%1.10e'%old)
        out.append(['%8.3f'%rad[i]] + ['%8.4e'%pres[i]] + ['%7.2f'%temp[i]] + out_abn)

print(out_abn)



# Save to dummy atm file
f = open(filename, 'w+')

f.write(header + '\n\n')
f.write(TP_params  + '\n\n')
f.write(fillers    + '\n\n')
f.write('#FINDSPEC\n' + out_spec + '\n\n')
f.write('#FINDTEA\n')
for i in np.arange(steps + 1):
    # Radius list
    f.write(out[i][0].rjust(10) + ' ')
        
    # Pressure list
    f.write(out[i][1].rjust(10) + ' ')
    
    # Temp list
    f.write(out[i][2].rjust(7) + ' ')
    
    # Dex abun list
    for j in np.arange(nspec):
        f.write(out[i][j+3].rjust(16)+' ')
    f.write('\n')
    
f.close()
