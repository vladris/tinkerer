# test runner
import glob
import os
import unittest

# save current directory and change working directory to test dir
cur_dir = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# glob all test cases
tests = [unittest.defaultTestLoader.loadTestsFromName(name[:-3]) for name in 
         glob.glob("test_*.py")]

# restore current directory
os.chdir(cur_dir)

# create a test suite and run it
testSuite = unittest.TestSuite(tests)

unittest.TextTestRunner().run(testSuite)

