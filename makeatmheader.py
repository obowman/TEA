#! /usr/bin/env python

# MAKEATMHEADER.PY
# To be used by runatm.py ONLY

import numpy as np
import re
import os

def makeatmheader(q, spec_list, pres_arr, temp_arr, atom_arr, desc):
    '''
    DOC
    '''
    temp     = float(temp_arr[q])
    pressure = float(pres_arr[q])
    n_atom   = np.size(atom_arr[0])
    # ### Obtain gdata file names and count
    gdata_files = os.listdir('gdata')
    n_gdata = np.size(gdata_files)
    n_spec = np.size(spec_list)
    
    # Create index of where species in inputs file are in gdata dir
    specindex = np.zeros(n_spec)
    for i in np.arange(n_spec):
        specfile = spec_list[i] + '.txt'
        if specfile in gdata_files:
            specindex[i] = gdata_files.index(specfile)
        else:
            print('Species ' + spec_list[i] + ' does not exist in /gdata! IGNORED THIS SPECIES.')
    
    # Create array of G/RT
    g_RT = np.zeros(n_spec)
    R = 8.3144621 #J/K/mol
    for i in np.arange(n_spec):
        specfile = 'gdata/' + gdata_files[np.int(specindex[i])]
        f = open(specfile, 'r')
        data = []
        headerline = True
        for line in f.readlines():
            if headerline:
                headerline = False
            else:
                l = [np.float(value) for value in line.split()]
                #print(l)
                data.append(l)
        
        f.close()
        data = np.asarray(data)
        idx = np.abs(data[:, 0] - temp).argmin()
        # Below is only necessary for H2O JANAF tables
        if (data[idx, 0] == data[-1, 0] and np.abs(data[idx, 0] - temp) > 100):
            #print(speclist[i] + ' NEEDED FIX')
            n_t = np.shape(data)[0]
            x = data[n_t-5:n_t, 0]
            y1 = data[n_t-5:n_t, 1]
            y2 = data[n_t-5:n_t, 2]
            print(y1, y2)       
            A1 = np.array([x, np.ones(5)])
            A2 = np.array([x, np.ones(5)])
            a1, b1 = np.linalg.lstsq(A1.T, y1)[0]
            a2, b2 = np.linalg.lstsq(A2.T, y2)[0]
            gdata_term1 = a1 * temp + b1
            gdata_term2 = a2 * temp + b2
        else:
            gdata_term1 = data[idx, 1]
            gdata_term2 = data[idx, 2]
        
        #print(gdata_term1, gdata_term2)
        # Equation is:
        #  G        G-H(298)      delta-f H(298)
        # ---  =    -------  +    --------------
        #  RT         RT                RT
        #
        # Ref: Eriksson 1971
        #
        # In below, need to convert to joules in second term (JANAF gives in kJ)
        #           First term already divided by T in JANAF
        
        g_RT[i] = - (gdata_term1 / R) + (gdata_term2 * 1000 / (temp * R))
    
    # ### Get number of elements used in species
    nostate = np.copy(spec_list)
    for i in np.arange(n_spec):
        nostate[i] = re.search('(.*?)_', spec_list[i]).group(1)
    
    # Get stoch information for species used
    stochfile = 'stoch.txt'
    f = open(stochfile, 'r')
    stochdata = []
    bline = True
    for line in f.readlines():
        l = [value for value in line.split()]
        stochdata.append(l)
    
    stochdata = np.asarray(stochdata)
    f.close()
    
    n_ele = np.size(stochdata[0, 1:])
    specstoch = np.empty((n_spec+1, n_ele), dtype=np.float)
    specstoch[0] = stochdata[0,1:]
    for i in np.arange(n_spec):
        idx = np.where(stochdata[:, 0] == nostate[i])[0]
        if np.size(idx) != 1:
            idx = idx[0]
        specstoch[i+1] = stochdata[idx,1:]
    
    # Determine which elements are used to trim down final stoch table
    is_used = np.empty(n_ele, dtype=np.bool)
    for j in np.arange(n_ele):
        if np.sum(specstoch[1:, j]) != 0:
            is_used[j] = True
        else:
            is_used[j] = False
    
    # Create final stoch table
    finalstoch = np.empty((n_spec + 2, np.sum(is_used) + 1), dtype=np.object)
    finalstoch[0,0] = 'b'
    for n in np.arange(np.sum(is_used)):
        cur_ele = stochdata[1, np.where(is_used)[0][n] + 1]
        for m in np.arange(n_atom):
            if atom_arr[0][m] == cur_ele:
                cur_abn = atom_arr[q][m]
        finalstoch[0,1+n] = cur_abn
    
    finalstoch[1,0] = 'Species'
    finalstoch[1,1:] = stochdata[1, np.where(is_used)[0] + 1]
    
    for i in np.arange(n_spec):
        finalstoch[i+2, 0] = spec_list[i]
        finalstoch[i+2, 1:] = map(int,specstoch[i+1, np.where(is_used)[0]])
    
    # Create output to be used as pipeline's header
    if not os.path.exists('headers/'): os.makedirs('headers/')
    outfile = 'headers/header_' + desc + ".txt"
    f = open(outfile, 'w+')
    f.write('== This is the input created for the main pipeline.  Contains species list, a and b values per specie, temperature of system in K, and pressure of system in atm. ==\n')
    f.write(np.str(pressure) + '\n')
    f.write(np.str(temp)     + '\n')
    f.write(np.str(finalstoch[0]).replace('[','').replace(']','') + '\n')
    for i in np.arange(n_spec):
        f.write(np.str(finalstoch[i+2]).replace('[','').replace(']','') + ' ')
        f.write(np.str(g_RT[i]).rjust(13) + '\n')
    
    f.close()
