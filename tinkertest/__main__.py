'''
    Test runner
    ~~~~~~~~~~~

    Used to run tests. 
    Run with no arguments will run all unittests.
    -v <mask> flag runs only tests matching mask (.py extension auto-appended)

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import argparse
import glob
import os
import unittest

# save current directory and change working directory to test dir
cur_dir = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", nargs=1, 
            help="run specific test(s): eg. -v test_rss runs only test_rss.py") 
command = parser.parse_args()

if command.v:
    mask = command.v[0] + ".py"
else:
    mask = "test_*.py"

# glob all test cases
tests = [unittest.defaultTestLoader.loadTestsFromName(name[:-3]) for name in 
         glob.glob(mask)]

# restore current directory
os.chdir(cur_dir)

# create a test suite and run it
testSuite = unittest.TestSuite(tests)

unittest.TextTestRunner().run(testSuite)

