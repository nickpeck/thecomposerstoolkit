import unittest

from . import coretests

def load_tests():
    test_suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromModule(coretests)
    test_suite.addTests(tests)
    return test_suite

if __name__ == '__main__':
   suite = load_tests()
   runner=unittest.TextTestRunner()
   runner.run(suite)