import numpy as np
import os


'''
Reads atm file and returns the data array contained within
'''
atm_file = "results/NOUSE/NOUSE.dat"
spec_mark = '#FINDSPEC'
tea_mark = '#FINDTEA'

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


lists = data.T

temp = lists[2][1:]

moles = np.zeros((np.size(spec_list), nrows))

