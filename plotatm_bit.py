import numpy as np
import matplotlib.pyplot as plt

plt.ion()

filename = 'dragtest.dat'
T, CO, CH4, H2O, N2, NH3= np.loadtxt(filename, dtype=float, comments='#', delimiter=None, converters=None, skiprows=13, usecols=(2, 8, 9, 10, 11, 12), unpack=True, ndmin=0)

plt.figure(1)
plt.clf()


plt.semilogy(T, CO , '-', color = 'r')
plt.semilogy(T, CH4, '-', color = 'k')
plt.semilogy(T, H2O, '-', color = 'cyan')
plt.semilogy(T, N2 , '-', color = 'g')
plt.semilogy(T, NH3, '-', color = 'b')

plt.legend()
plt.ylim(-10, -2)
plt.xlim(100, 3000)

