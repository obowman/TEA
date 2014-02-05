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

# User inputs
spec        = "C H O N"        # Atomic label for input abundances
solids      = True
#pres_erange = (-5, 2)          # Range for exponents on pressure
steps       = 100               # Number of steps in pressure
TP_params   = [1, 2, 3, 4, 5, 
               6, 7, 8, 9, 0]  # Dummy TP profile params
T           = np.linspace(100, 3000, steps)
fillers     = '''\n# FILLER STUFF HERE\n'''                   # Filler to save space
filename    = 'TEBS-Solids-after.dat'   # Output atm file name
abun        = 'abundances.txt' # Input abundances (solar for this case)
header      = "# This is a NO-USE pre-TEA atmosphere file.\n\
# TEA accepts a file in this format to produce \n\
# abundances as a function of pressure and temperature.\n\n"

# read abundance data
f = open(abun, 'r')
abundata = []
for line in f.readlines():
    l = [value for value in line.split()]
    abundata.append(l)

abundata = np.asarray(abundata)
f.close()

# Trim abundata to the stuff we care about
spec   = spec.split(" ")
nspec  = np.size(spec)
lookat = np.zeros(abundata.shape[0], dtype=bool)

for i in np.arange(nspec):
    lookat += (abundata[:,1] == spec[i])

abun_trim = abundata[lookat]

# Also read Si abundance (For Burrows Sharp 1999 quick fix)
Si_abun = (abundata[:,1] == 'Si')

# Get pressure range
#l, u = pres_erange[0], pres_erange[1]
rad  = np.arange(steps)[::-1] * 1000
#pres = np.logspace(l, u, steps)
pres = np.ones(steps)
temp = np.ones(steps) * T

# Create array that will be in output atm file...
out_spec = abun_trim[:,1].tolist()
out_dex  = abun_trim[:,2].tolist()
print(out_dex)
out_dex  = map(float, abun_trim[:,2])
out_num  = 10**np.array(out_dex)
out_abn  = (out_num / np.sum(out_num)).tolist()

#Implimenting solid quick fix Burrows Sharp 1999
Si_frac = 10**Si_abun[0] / np.sum(out_num)

for n in np.arange(np.size(out_abn)):
    out_abn[n] = str('%1.10e'%out_abn[n])

    
out = [['    Radius'] + ['Pressure'] + ['Temp'] + out_spec]

#new_abn = np.copy(out_abn)
#print(new_abn)


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

f.write(header)
f.write(str(TP_params).strip('[]') + '\n')
f.write(fillers + '\n')
f.write('#FINDSPEC\n\
H_g C_g N_g O_g H2_ref CO_g CH4_g H2O_g N2_ref NH3_g\n\n')
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
        f.write(out[i][j+3].rjust(10)+' ')
    f.write('\n')
    
f.close()
