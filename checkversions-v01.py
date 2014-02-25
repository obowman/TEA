#! /usr/bin/env python

# Module to check versions of programs used by TEA.

# List of imports:
'''
# Iterate
from numpy import size
from numpy import where
from multiprocessing import Process, Queue
#from sys import stdout
from sys import argv
from sys import stdout
from ast import literal_eval

# Lagrange
import numpy as np
from sympy.core import Symbol
from sympy.solvers import solve
import os

# Lambdacorr
import numpy as np
'''
import time
start = time.time()

# Imports used in TEA
import numpy
import os
import multiprocessing
import sys
import ast
import sympy

end = time.time()
elapsed = end - start

# Open log file
file = 'version-info.txt'
f = open(file, 'w+')

print("Import time: " + str(elapsed) + " seconds.\n")
f.write("Import time: " + str(elapsed) + " seconds.\n\n")

# Retrieve versions
py  = sys.version
ast = ast.__version__
mp  = multiprocessing.__version__
npy = numpy.__version__
sym = sympy.__version__

print("Python: " + py)
print("AST:    " + ast)
print("MultiP: " + mp)
print("Numpy:  " + npy)
print("Sympy:  " + sym)

f.write("Python: " + py + '\n')
f.write("AST:    " + ast + '\n')
f.write("MultiP: " + mp  + '\n')
f.write("Numpy:  " + npy + '\n')
f.write("Sympy:  " + sym + '\n')



# Memory check
import ctypes
class memoryCheck():
    """Checks memory of a given system"""

    def __init__(self):

        if os.name == "posix":
            self.value = self.linuxRam()
        elif os.name == "nt":
            self.value = self.windowsRam()
        else:
            print "I only work with Win or Linux :P"

    def windowsRam(self):
        """Uses Windows API to check RAM in this OS"""
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ("dwLength", c_ulong),
                ("dwMemoryLoad", c_ulong),
                ("dwTotalPhys", c_ulong),
                ("dwAvailPhys", c_ulong),
                ("dwTotalPageFile", c_ulong),
                ("dwAvailPageFile", c_ulong),
                ("dwTotalVirtual", c_ulong),
                ("dwAvailVirtual", c_ulong)
            ]
        memoryStatus = MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))

        return int(memoryStatus.dwTotalPhys/1024**2)

    def linuxRam(self):
        """Returns the RAM of a linux system"""
        totalMemory = os.popen("free -m").readlines()[1].split()[1]
        return int(totalMemory)

mem = memoryCheck().value

print("\nAvailable memory: " + str(mem))
f.write("\nAvailable memory: " + str(mem) + '\n')


# Processor info
import platform, subprocess
def get_processor_info():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        return subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        return subprocess.check_output(command, shell=True).strip()
    return ""


print("Processor: " + get_processor_info() + '\n')
f.write("Processor: " + get_processor_info() + '\n')

f.close()
