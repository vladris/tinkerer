'''
    Test runner
    ~~~~~~~~~~~

    Used to run tests. 
    Run with no arguments will run all unittests.
    -v <mask> flag runs only tests matching mask (.py extension auto-appended)
    -t, --theme builds a test blog with the given theme
    -c, --clean cleans up test directory

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import argparse
import glob
import os
import unittest
import tinkertest.utils

# save current directory and change working directory to test dir
cur_dir = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", nargs=1, 
            help="run specific test(s): eg. -v test_rss runs only test_rss.py") 
parser.add_argument("-t", "--theme", nargs=1,
            help="build test blog with given theme")
parser.add_argument("-c", "--clean", action="store_true",
            help="clean up test directory")

# process command line
command = parser.parse_args()

if command.theme:
    tinkertest.utils.build_theme(command.theme[0])
elif command.clean:
    tinkertest.utils.cleanup()
else:
    if command.v:
        mask = command.v[0] + ".py"
    else:
        mask = "test_*.py"

    # glob all test cases
    tests = [unittest.defaultTestLoader.loadTestsFromName(name[:-3]) for name in 
             glob.glob(mask)]

    # create a test suite and run it
    testSuite = unittest.TestSuite(tests)

    unittest.TextTestRunner().run(testSuite)

# restore current directory
os.chdir(cur_dir)


