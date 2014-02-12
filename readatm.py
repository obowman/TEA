# Testing to read atm file for TEA

import numpy as np
import os

def readatm(atm_file, spec_mark = '#FINDSPEC', tea_mark = '#FINDTEA'):
    '''
    Reads atm file and returns the data array contained within
    '''
    file = os.getcwd() + '/' + atm_file
    
    f = open(file, 'r')
    info = []
    for line in f.readlines():
        l = [value for value in line.split()]
        info.append(l)
    
    f.close()
    
    marker = np.zeros(2, dtype=int) # FINDSPEC marker, FINDTEA marker
    ninfo  = np.size(info)          # Number of rows in file
    
    for i in np.arange(ninfo):
        if info[i] == [spec_mark]:
            marker[0] = i + 1
        if info[i] == [tea_mark]:
            marker[1] = i + 1
    
    spec_list  = info[marker[0]]       # Retrieve species list
    
    data_label = np.array(info[marker[1]]) # Retrieve labels for data array
    ncols      = np.size(data_label)   # Number of labels in data array
    nrows      = ninfo - marker[1]     # Number of lines to read for data table (inc. label)    
    
    data = np.empty((nrows, ncols), dtype=np.object)
    
    for i in np.arange(nrows):
        data[i] = np.array(info[marker[1] + i])
    
    # FINDME: Account for if format of atm file changes.  It shouldn't!
    iradi = np.where(data_label == 'Radius'  )[0][0]
    ipres = np.where(data_label == 'Pressure')[0][0]
    itemp = np.where(data_label == 'Temp'    )[0][0]
    iatom = 3 # Will always be last in table, after three other columns
    
    radi_arr = data[:,iradi]      # Won't be passed into TEA
    pres_arr = data[:,ipres]      # WILL  be passed into TEA
    temp_arr = data[:,itemp]      # WILL  be passed into TEA
    atom_arr = data[:,iatom:]     # WILL  be passed into TEA
    
    n_runs = data.shape[0]  # Number of times TEA will have to execute
    
    return n_runs, spec_list, radi_arr, pres_arr, temp_arr, atom_arr, marker[1]
