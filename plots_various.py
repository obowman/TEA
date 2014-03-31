import numpy as np
import matplotlib.pyplot as plt
import os

# #############################################################
# #####################
# ### PLOT ATM FILE ###
# #####################

dir = os.getcwd()

filename = '/results/NewStartTest3/NewStartTest3.dat'
T, CO, CH4, H2O, N2, NH3 = np.loadtxt(dir + filename, dtype=float, comments='#', delimiter=None, converters=None, skiprows=13, usecols=(2, 8, 9, 10, 11, 12), unpack=True, ndmin=0)

plt.ion()
plt.figure(1)
plt.clf()

# H2O condensate below 273 K
H2O[T < 273] = 1e-50

plt.plot(T, np.log10(CO ), 'r-', label="Explore")
plt.plot(T, np.log10(CH4), '-', color = 'k')
plt.plot(T, np.log10(H2O), '-', color = 'cyan')
plt.plot(T, np.log10(N2 ), '-', color = 'g')
plt.plot(T, np.log10(NH3), '-', color = 'b')

plt.title('NewStartTest3', fontsize=14)
plt.xlabel('T [K]'                  , fontsize=14)
plt.ylabel('log10 Mixing Fraction' , fontsize=14)
plt.legend(loc='lower center', prop={'size':10})
plt.ylim(-10, -2)
plt.xlim(100, 3000)
plt.savefig("NewStartTest(withoutnew)")
'''


# Overplot
dir = os.getcwd()
filename = '/results/EndMarTest/EndMarTest.dat'
T, CO, CH4, H2O, N2, NH3 = np.loadtxt(dir + filename, dtype=float, comments='#', delimiter=None, converters=None, skiprows=13, usecols=(2, 8, 9, 10, 11, 12), unpack=True, ndmin=0)

#plt.ion()
#plt.figure(1)
#plt.clf()

# H2O condensate below 273 K
H2O[T < 273] = 1e-50

plt.plot(T, np.log10(CO ), 'r+', label="No explore")
plt.plot(T, np.log10(CH4), '+', color = 'k')
plt.plot(T, np.log10(H2O), '+', color = 'cyan')
plt.plot(T, np.log10(N2 ), '+', color = 'g')
plt.plot(T, np.log10(NH3), '+', color = 'b')

plt.xlim(100, 3000)
plt.ylim(-10, -2)

plt.title('EndMarTestCompare', fontsize=14)
plt.xlabel('T [K]'                  , fontsize=14)
plt.ylabel('log10 Mixing Fraction' , fontsize=14)
plt.legend(loc='lower center', prop={'size':10})
plt.ylim(-10, -2)
plt.xlim(100, 3000)
plt.savefig("EndMarTestCompare")





# #############################################################
# #########################
# ### PLOT JANAF VALUES ###
# #########################

dir = os.getcwd() + '/outputs/'
desc = "checkJANAF/"
files = np.array([])
for i in np.arange(np.size(T)):
    files = np.append(files, dir + desc + "JANAF_check_" + '%.0f'%T[i] + 'K.txt')

plt.ion()
plt.figure(2)
plt.clf()

plt.xlabel('Temperature')
plt.ylabel('g_RT Values')
plt.title('g_RT values vs. Temperature')
for i in np.arange(np.size(T)):
    stuff = np.loadtxt(files[i], dtype =str, delimiter=None, unpack=True, ndmin=0)
    for k in np.arange(stuff[0].size):
        if stuff[0][k] == 'CO_g':
            plt.plot(T[i], stuff[1][k], 'r.')
        if stuff[0][k] == 'CH4_g':
            plt.plot(T[i], stuff[1][k], 'k.')
        if stuff[0][k] == 'H2O_g':
            plt.plot(T[i], stuff[1][k], 'c.')
        if stuff[0][k] == 'N2_ref':
            plt.plot(T[i], stuff[1][k], 'g.')
        if stuff[0][k] == 'NH3_g':
            plt.plot(T[i], stuff[1][k], 'b.')

plt.show()



'''