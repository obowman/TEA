import re
import numpy as np

# This gets the elemental weight of each element in the specie. Only works up to Mo (JANAF limit)
def comp(specie):
    '''
    DESC HERE
    '''
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
    n_ele = np.size(symbols)
    
    elements = np.empty((n_ele, 3), dtype=np.object)
    elements[:, 0] = np.arange(n_ele)
    elements[:, 1] = symbols
    elements[:, 2] = 0
    
    if specie == 'NOUSE':
        return elements
    
    chars = len(specie)
    iscaps  = np.empty(chars, dtype=np.bool)
    isdigit = np.empty(chars, dtype=np.bool)
    for i in np.arange(len(specie)):
        iscaps[i] = (re.findall('[A-Z]', specie[i]) != [])
        isdigit[i] = specie[i].isdigit()
    
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
