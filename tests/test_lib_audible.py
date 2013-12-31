import unittest
import lib_audible

class Test(unittest.TestCase):
    def test_set_author(self):
        lib_audible._set_author_span()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()