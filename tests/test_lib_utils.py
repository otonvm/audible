import unittest

import lib.lib_utils as lib_utils

class Test(unittest.TestCase):
    def test_yn_query(self):
        def get_input(message):
            return 'y'
        lib_utils.get_input = get_input
        self.assertEqual(lib_utils.yn_query("none"), True)

        def get_input(message):
            return 'n'
        lib_utils.get_input = get_input
        self.assertEqual(lib_utils.yn_query("none"), False)

        def get_input(message):
            return ''
        lib_utils.get_input = get_input
        self.assertEqual(lib_utils.yn_query("none"), True)

if __name__ == "__main__":
    unittest.main()
