import numpy as np
import os
import re

from ast import literal_eval
from sys import argv
from sys import stdout

#print('Format imports...')


#errorprint = literal_eval(argv[1:][0])


# Current contents:
#       makeheader: Reads in three different inputs to create header file for pipeline.
#                   Inputs: 
#       readheader: Reads the header file for the pipeline.
#       readoutput: Reads output files produced and used by the pipeline.
#           output: Write same output as fancyout, but in machine readable format. Use this 
#                    in the pipeline!
#    output_nocorr: Same as output, but before lambda correction.
#   output_results: Same as output, but only for the final results.
#         fancyout: Prints in-shell and external table of values so they are easily readable
#                    by the human eye. NOT FOR PIPELINE INPUT!
#  fancyout_nocorr: Same as fancyout, but before lambda correction.
# fancyout_results: Same as fancyout, but for the final results.


def readheader(file, fromatm=False, dex=False):
    '''
    DESC
    '''
    if fromatm:
        return 'foo'
    else:
        f = open(file, 'r+')
        l = 0
        speclist = []
        a = [[]]
        c = []
        for line in f.readlines():
            if (l == 1):
                pressure = np.float([value for value in line.split()][0])
            #if (l == 2):
            #    j = np.int([value for value in line.split()][0])
            if (l == 2):
                temp = np.float([value for value in line.split()][0])
            if (l == 3):
                val = [value for value in line.split()]
                b   = [float(u) for u in val[1:]]
            if (l == 4):
                val = [value for value in line.split()]
                speclist = np.append(speclist, val[0])
                a = [[int(u) for u in val[1:-1]]]
                c = np.float(val[-1])
            if (l > 4):
                val = [value for value in line.split()]
                speclist = np.append(speclist, val[0])
                a = np.append(a, [[int(u) for u in val[1:-1]]], axis=0)
                c = np.append(c, np.float(val[-1]))
            l += 1
        
        i = speclist.size
        j = a.shape[1]
        f.close()
    
    if dex:
        b_10 = 10**np.array(b)
        b    = np.array((b_10 / np.sum(b_10)).tolist())
    # FINDME: Testing for initial number of moles times b
    multiplier = 1
    b = (np.array(b) * multiplier).tolist()
    
    return pressure, temp, i, j, speclist, a, b, c


def readoutput(file):
    '''
    DESC
    '''
    f = open(file, 'r')
    data = []
    for line in f.readlines():
        l = [value for value in line.split()]
        data.append(l)
    
    f.close()
    
    header    = data[0][0]
    it_num    = np.array(data[1]).astype(np.int)[0]
    speclist  = np.array(data[2]).astype(np.str)
    y         = np.array(data[3]).astype(np.float)
    x         = np.array(data[4]).astype(np.float)
    delta     = np.array(data[5]).astype(np.float)
    y_bar     = np.array(data[6]).astype(np.float)[0]
    x_bar     = np.array(data[7]).astype(np.float)[0]
    delta_bar = np.array(data[8]).astype(np.float)[0]
    
    return(header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar)


def output(datadir, header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint):
    ''' 
    Output formats are as follows, in this order:
       header :   (string) : Name of header file used
       it_num :  (integer) : Iteration number
     speclist : (str list) : Names of species ordered by 'i'
            y :    (array) : Initial mol values of species 'i'
            x :    (array) : Final mol values of species 'i'
        delta :    (array) : Change in mol values of species 'i'
        y_bar :    (float) : Total initial mol of all species
        x_bar :    (float) : Total final mol of all species
    detla_bar :    (float) : Change in total mol of all species
    '''
    
    file = datadir + '/lagrange-iteration-' + np.str(it_num) + '.txt'
    f = open(file, 'w+')

    i = speclist.size
    
    f.write(header + '\n') # 1st row
    
    f.write(np.str(it_num) + '\n') # 2nd row
    
    for n in np.arange(i):    # 3rd row
        f.write(speclist[n] + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 4th row
        f.write(np.str(y[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 5th row
        f.write(np.str(x[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 6th row
        f.write(np.str(delta[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    f.write(np.str(y_bar) + '\n') # 7th row
    f.write(np.str(x_bar) + '\n') # 8th row
    f.write(np.str(delta_bar) + '\n') # 9th row
    
    f.close()
    if doprint == True:
        print('\n\nMade file \'' + file + '\' containing machine data.')


def output_nocorr(datadir, header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint):
    ''' 
    Output formats are as follows, in this order:
       header :   (string) : Name of header file used
       it_num :  (integer) : Iteration number
     speclist : (str list) : Names of species ordered by 'i'
            y :    (array) : Initial mol values of species 'i'
            x :    (array) : Final mol values of species 'i'
        delta :    (array) : Change in mol values of species 'i'
        y_bar :    (float) : Total initial mol of all species
        x_bar :    (float) : Total final mol of all species
    detla_bar :    (float) : Change in total mol of all species
    '''
    
    file = datadir + '/lagrange-iteration-' + np.str(it_num) + '-nocorr.txt'
    f = open(file, 'w+')

    i = speclist.size
    
    f.write(header + '\n') # 1st row
    
    f.write(np.str(it_num) + '\n') # 2nd row
    
    for n in np.arange(i):    # 3rd row
        f.write(speclist[n] + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 4th row
        f.write(np.str(y[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 5th row
        f.write(np.str(x[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 6th row
        f.write(np.str(delta[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    f.write(np.str(y_bar) + '\n') # 7th row
    f.write(np.str(x_bar) + '\n') # 8th row
    f.write(np.str(delta_bar) + '\n') # 9th row
    
    f.close()
    if doprint == True:
        print('\n\nMade file \'' + file + '\' containing machine data.')


def output_results(datadir, header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint):
    ''' 
    Output formats are as follows, in this order:
       header :   (string) : Name of header file used
       it_num :   integer) : Iteration number
     speclist : (str list) : Names of species ordered by 'i'
            y :    (array) : Initial mol values of species 'i'
            x :    (array) : Final mol values of species 'i'
        delta :    (array) : Change in mol values of species 'i'
        y_bar :    (float) : Total initial mol of all species
        x_bar :    (float) : Total final mol of all species
    detla_bar :    (float) : Change in total mol of all species
    '''
    if not os.path.exists(datadir): os.makedirs(datadir)
    file = datadir + '/results-machine-read.txt'
    f = open(file, 'w+')

    i = speclist.size
    
    f.write(header + '\n') # 1st row
    
    f.write(np.str(it_num) + '\n') # 2nd row
    
    for n in np.arange(i):    # 3rd row
        f.write(speclist[n] + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 4th row
        f.write(np.str(y[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 5th row
        f.write(np.str(x[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    for n in np.arange(i):    # 6th row
        f.write(np.str(delta[n]) + ' ')
        if n == (i-1): f.write('\n')
    
    f.write(np.str(y_bar) + '\n') # 7th row
    f.write(np.str(x_bar) + '\n') # 8th row
    f.write(np.str(delta_bar) + '\n') # 9th row
    
    f.close()
    if doprint == True:
        print('\n\nMade file \'' + file + '\' containing final machine data.')


def fancyout(datadir, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint):
    ''' 
    Output formats are as follows:
            i : integer (number of species)
     speclist : list of strings (species name in order of ascending i)
            y : array (yi in order of ascending i)
            x : array (xi in order of ascending i)
        delta : array (delta in order of ascending i)
        y_bar : float (y_bar)
        x_bar : float (x_bar)
    delta_bar : float (delta_bar)
    '''
    
    file = datadir + '/lagrange-iteration-' + np.str(it_num) + '-NOUSE.txt'
    f = open(file, 'w+')
    f.write('This .txt file is for visual use only.  DO NOT USE FOR ITERATIONS!\n')
    f.write('Data for iteration #' + np.str(it_num) + '\n\n')
    
    i = speclist.size
    for n in np.arange(i):
        if n == 0:
            f.write('All units are in mol \n')
            f.write('Species |'.rjust(10) + 'y_i |'.rjust(12) + 'x_i |'.rjust(12) + 'delta \n'.rjust(12)) 
        xs  = '%8.6f'%x[n]
        ys  = '%8.6f'%y[n] 
        ds  = '%8.6f'%delta[n]
        xbs = '%8.6f'%x_bar
        ybs = '%8.6f'%y_bar
        dbs = '%8.6f'%delta_bar
        name = speclist[n]  
        f.write(name.rjust(8) + ' |' + ys.rjust(10) + ' |' + xs.rjust(10) + ' |' +ds.rjust(10) + '\n')
        if n == (i-1):
            f.write('\n')
            f.write('y_bar : '.rjust(35) + ybs.rjust(9) + '\n')
            f.write('x_bar : '.rjust(35) + xbs.rjust(9) + '\n')
            f.write('delta_bar : '.rjust(35) + dbs.rjust(9) + '\n')
    f.close()
    
    if doprint == True:
        f = open(file, 'r+')
        h = 0
        for line in f:
            if h == 0:
                print('Made file \'' + file + '\' containing the following:')
            else:
                line = line.strip('\n')
                print(line)
            h += 1
        
        f.close()

    
def fancyout_nocorr(datadir, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, doprint):
    ''' 
    Output formats are as follows:
            i : integer (number of species)
     speclist : list of strings (species name in order of ascending i)
            y : array (yi in order of ascending i)
            x : array (xi in order of ascending i)
        delta : array (delta in order of ascending i)
        y_bar : float (y_bar)
        x_bar : float (x_bar)
    delta_bar : float (delta_bar)
    '''
    
    file = datadir + '/lagrange-iteration-' + np.str(it_num) + '-NOUSE-nocorr.txt'
    f = open(file, 'w+')
    f.write('This .txt file is for visual use only.  DO NOT USE FOR ITERATIONS!\n')
    f.write('Data for iteration #' + np.str(it_num) + ', pre-correction for negative mole values.\n\n')
    
    i = speclist.size
    for n in np.arange(i):
        if n == 0:
            f.write('All units are in mol \n')
            f.write('Species |'.rjust(10) + 'y_i |'.rjust(12) + 'x_i |'.rjust(12) + 'delta \n'.rjust(12)) 
        xs  = '%8.6f'%x[n]
        ys  = '%8.6f'%y[n] 
        ds  = '%8.6f'%delta[n]
        xbs = '%8.6f'%x_bar
        ybs = '%8.6f'%y_bar
        dbs = '%8.6f'%delta_bar
        name = speclist[n]  
        f.write(name.rjust(8) + ' |' + ys.rjust(10) + ' |' + xs.rjust(10) + ' |' +ds.rjust(10) + '\n')
        if n == (i-1):
            f.write('\n')
            f.write('y_bar : '.rjust(35) + ybs.rjust(9) + '\n')
            f.write('x_bar : '.rjust(35) + xbs.rjust(9) + '\n')
            f.write('delta_bar : '.rjust(35) + dbs.rjust(9) + '\n')
    f.close()
    
    if doprint == True:
        f = open(file, 'r+')
        h = 0
        for line in f:
            if h == 0:
                print('Made file \'' + file + '\' containing the following:')
            else:
                line = line.strip('\n')
                print(line)
            h += 1
        
        f.close()


def fancyout_results(datadir, header, it_num, speclist, y, x, delta, y_bar, x_bar, delta_bar, pressure, temp, doprint):
    if not os.path.exists(datadir): os.makedirs(datadir)
    file = datadir + '/results-visual.txt'
    f = open(file, 'w+')
    f.write('This .txt file is for visual use only.\n')
    f.write('These results are for the "' + header + '" run.\n')
    f.write('Iterations complete after ' + np.str(it_num) + ' runs at ' + np.str(pressure) + ' atm and ' + np.str(temp) + 'K. Final computation:\n\n')
    
    i = speclist.size
    for n in np.arange(i):
        if n == 0:
            f.write('All units are in mol \n')
            f.write('Species |'.rjust(10) + 'Initial x |'.rjust(16) + 'Final x |'.rjust(16) + 'Delta |'.rjust(16) + 'Final Abun \n'.rjust(16)) 
        xs  = '%8.10f'%x[n]
        ys  = '%8.10f'%y[n] 
        ds  = '%8.10f'%delta[n]
        xbs = '%8.10f'%x_bar
        ybs = '%8.10f'%y_bar
        dbs = '%8.10f'%delta_bar
        # FINDME
        abn_float = x[n] / x_bar
        abn = '%8.7e'%abn_float
        name = speclist[n]  
        f.write(name.rjust(8) + ' |' + ys.rjust(14) + ' |' + xs.rjust(14) + ' |' +ds.rjust(14) + ' |' +abn.rjust(14) + '\n')
        if n == (i-1):
            f.write('\n')
            f.write('Initial Total Mol : '.rjust(35) + ybs.rjust(9) + '\n')
            f.write('Final Total Mol : '.rjust(35) + xbs.rjust(9) + '\n')
            f.write('Change in Total Mol : '.rjust(35) + dbs.rjust(9) + '\n')
    f.close()

    if doprint == True:
        f = open(file, 'r+')
        h = 0
        for line in f:
            if h == 0:
                print('Made file \'' + file + '\' containing the following:')
            else:
                line = line.strip('\n')
                print(line)
            h += 1
        
        f.close()

def cleanup(datadir, it_num, clean):
    """
    DOC
    """
    if (it_num >= 2) & (clean):
        #print('Removing ' + str(it_num-1))
        if os.path.isfile(datadir + "/lagrange-iteration-" + np.str(it_num-1) + "-nocorr.txt"):
            os.remove(datadir + "/lagrange-iteration-" + np.str(it_num-1) + "-nocorr.txt")
        if os.path.isfile(datadir + "/lagrange-iteration-" + np.str(it_num-1) + ".txt"):
            os.remove(datadir + "/lagrange-iteration-" + np.str(it_num-1) + ".txt")
        if os.path.isfile(datadir + "/lagrange-iteration-" + np.str(it_num-1) + "-NOUSE-nocorr.txt"):
            os.remove(datadir + "/lagrange-iteration-" + np.str(it_num-1) + "-NOUSE-nocorr.txt")
        if os.path.isfile(datadir + "/lagrange-iteration-" + np.str(it_num-1) + "-NOUSE.txt"):
            os.remove(datadir + "/lagrange-iteration-" + np.str(it_num-1) + "-NOUSE.txt")

def printout(str, it_num = False):
    stdout.write('\r\n')
    if np.bool(it_num):
        stdout.write(str % it_num)
    else:
        stdout.write(str)
    stdout.flush()

def output_atm():
    header      = "# This is a NO-USE pre-TEA atmosphere file.\n\
# TEA accepts a file in this format to produce \n\
# abundances as a function of pressure and temperature.\n\n"
    filename = desc + '.dat'
    f = open(filename, 'w+')
    
    f.write(header)
    f.write(str(TP_params).strip('[]') + '\n')
    f.write(fillers + '\n')
    f.write('#FINDSPEC\n\
    H_g H2_ref H2O_l-g N_g NH_g NO_g N2_ref O_g OH_g O2_ref\n\n')
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
#END