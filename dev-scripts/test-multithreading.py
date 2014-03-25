import multiprocessing as mp
import sys, os

from multiprocessing import Process

print("I'm in main module")
# OSGeo4W does not bundle python in exec_prefix for python
path = os.path.abspath(os.path.join(sys.exec_prefix, '../../bin/pythonw.exe'))
mp.set_executable(path)
print("Setting executable path to {:s}".format(path))
sys.argv = [ None ]               # '../tst.py' __file__
mgr = mp.Manager()
print("I'm past Manager()")