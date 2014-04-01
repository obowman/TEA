'''
comp.py

============
Description
============

     Species counting function in order to count the number of each element 
  in a chemical species.  Takes in a string of a chemical species (i.e., "H2O") 
  and returns an array containing every element with corresponding counts found 
  in that species.


============
Inputs
============

specie : string :
      Chemical species in the format "atomic symbol, count, etc" such that the 
  number of counts is always directly following the corresponding atomic symbol.
  'specie' string can contain redundancies, but not parantheses. Names should 
  match the "JCODE" formulas listed in the NIST JANAF Tables listed at: 
                     kinetics.nist.gov/janaf/formula.html

      If 'specie' is "NOUSE", function will return an array of all 0 counts.


============
Outputs
============

elements : 2D array :
      Array containing three columns of equal length: the first column is a 
    full list of all elements' atomic numbers from deuterium (#0) up to 
    copernicium (#112), the second column contains the corresponding atomic 
    symbol, and the third column counts of each of these elements found in the
    input species.


============
Examples
============

>>> from comp import comp
>>> species = "H2O"        # water 'JCODE'
>>> comp(species)
array([[0, D, 0],
       [1, H, 2],
       [2, He, 0],
       [3, Li, 0],
       [4, Be, 0],
       [5, B, 0],
       [6, C, 0],
       [7, N, 0],
       [8, O, 1],
       ...
       [112, Cn, 0]], dtype=object)
>>>
>>> species = "C2N2" # Ethanedinitrile 'JCODE'
>>> comp("C2N2")
array([[0, D, 0],
       [1, H, 0],
       [2, He, 0],
       [3, Li, 0],
       [4, Be, 0],
       [5, B, 0],
       [6, C, 2],
       [7, N, 2],
       ...
       [112, Cn, 0]], dtype=object)
>>>
>>> species = "C1C2C3" # Dummy example
>>> comp(species)
array([[0, D, 0],
       [1, H, 0],
       [2, He, 0],
       [3, Li, 0],
       [4, Be, 0],
       [5, B, 0],
       [6, C, 6],
       [7, N, 0],
       ...
       [112, Cn, 0]], dtype=object)
>>>


============
Revisions
============

v1.0.0 | 2014-04-01 | bowman@knights.ucf.edu | Updated documentation.
v1.0.0 | 2013-02-13 | bowman@knights.ucf.edu | Added full functionality for JCODE.
v0.0.1 | 2013-02-05 | bowman@knights.ucf.edu | Initial version.
'''


import re
import numpy as np

# This gets the elemental weight of each element in the specie. Uses JCODE 
# species values given from NIST JANAF tables, linked in description.
def comp(specie):
    # List of each atomic species' symbols.  Start with deuterium, end with 
    # copernicium.
    symbols = np.array([
    'D',
    'H',
    'He',
    'Li',
    'Be',
    'B',
    'C',
    'N',
    'O',
    'F',
    'Ne',
    'Na',
    'Mg',
    'Al',
    'Si',
    'P',
    'S',
    'Cl',
    'Ar',
    'K',
    'Ca',
    'Sc',
    'Ti',
    'V',
    'Cr',
    'Mn',
    'Fe',
    'Co',
    'Ni',
    'Cu',
    'Zn',
    'Ga',
    'Ge',
    'As',
    'Se',
    'Br',
    'Kr',
    'Rb',
    'Sr',
    'Y',
    'Zr',
    'Nb',
    'Mo',
    'Tc',
    'Ru',
    'Rh',
    'Pd',
    'Ag',
    'Cd',
    'In',
    'Sn',
    'Sb',
    'Te',
    'I',
    'Xe',
    'Cs',
    'Ba',
    'La',
    'Ce',
    'Pr',
    'Nd',
    'Pm',
    'Sm',
    'Eu',
    'Gd',
    'Tb',
    'Dy',
    'Ho',
    'Er',
    'Tm',
    'Yb',
    'Lu',
    'Hf',
    'Ta',
    'W',
    'Re',
    'Os',
    'Ir',
    'Pt',
    'Au',
    'Hg',
    'Tl',
    'Pb',
    'Bi',
    'Po',
    'At',
    'Rn',
    'Fr',
    'Ra',
    'Ac',
    'Th',
    'Pa',
    'U',
    'Np',
    'Pu',
    'Am',
    'Cm',
    'Bk',
    'Cf',
    'Es',
    'Fm',
    'Md',
    'No',
    'Lr',
    'Rf',
    'Db',
    'Sg',
    'Bh',
    'Hs',
    'Mt',
    'Ds',
    'Rg',
    'Cn' ])
    
    # Count elements
    n_ele = np.size(symbols)
    
    # Create 2D array containing all symbols, atomic numbers, and counts
    elements = np.empty((n_ele, 3), dtype=np.object)
    elements[:, 0] = np.arange(n_ele)
    elements[:, 1] = symbols
    elements[:, 2] = 0
    
    # Scenario for returning empty array
    if specie == 'NOUSE':
        return elements
    
    # Begin counting elements in string
    chars = len(specie)
    iscaps  = np.empty(chars, dtype=np.bool)
    isdigit = np.empty(chars, dtype=np.bool)
    for i in np.arange(len(specie)):
        iscaps[i] = (re.findall('[A-Z]', specie[i]) != [])
        isdigit[i] = specie[i].isdigit()
    
    # Circumstances for ending each count
    endele = True
    result = [[]]
    for i in np.arange(len(specie)):
        iscaps[i] = (re.findall('[A-Z]', specie[i]) != [])
        isdigit[i] = specie[i].isdigit()
        if endele == True:
            ele = ''
            weight = 0
            endele = False
        if (isdigit[i] == False): 
            # Check if char is digit
            ele += specie[i]
        if isdigit[i] == True:
            weight = np.int(specie[i])
        if (isdigit[i] == False and (iscaps[i+1:i+2] == True or i == chars-1)):
            weight = 1
        if (iscaps[i+1:i+2] == True or i == chars-1): 
            # Check if this is the end of the element name or isdigit[i+1:i+2] == True 
            endele = True
        if endele == True:
            index = np.where(elements[:, 1] == ele)[0]
            elements[index, 2] += weight
            if result == [[]]:
                result = np.append(result, [[ele, weight]], axis=1)
            else:
                result = np.append(result, [[ele, weight]], axis=0)
    
    return elements
