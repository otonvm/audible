import unittest
import lib.lib_audible

class Test(unittest.TestCase):
    inst = lib.lib_audible.Metadata
    
    def test_set_date(self):
        inst._set_date_span()


if __name__ == "__main__":
    unittest.main()