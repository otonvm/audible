import unittest

import os
import sys
import subprocess
import platform
import pickle

import lib.lib_mux as lib_mux


if platform.system() == "Windows":
    mp4boxbin = os.path.abspath(__file__)[:-22]
    mp4boxbin = os.path.join(mp4boxbin, "tools\win\mp4box.exe")
    mp4boxpkl = "tests/mp4box_output_win.pkl"
else:
    mp4boxbin = os.path.abspath(__file__)[:-22]
    mp4boxbin = os.path.join(mp4boxbin, "tools/mac/MP4Box")
    mp4boxpkl = "tests/mp4box_output_mac.pkl"

with open(mp4boxpkl, mode='rb') as file:
    mp4box_output = pickle.load(file)


class Test(unittest.TestCase):

    def test_bin_found(self):
        cls = lib_mux.MP4Box()
        with self.assertRaises(FileNotFoundError):
            cls.set_path("none")
            cls._test_bin_exists()

    def test_bin_found2(self):
        cls = lib_mux.MP4Box()
        with self.assertRaises(FileNotFoundError):
            cls.set_path("none")
            cls._test_bin_exists()

    def test_bin_timeout(self):
        cls = lib_mux.MP4Box()
        with self.assertRaises(subprocess.SubprocessError):
            cls._cmd = [sys.executable, "-c", "import time; time.sleep(3)"]
            cls._test_bin_works()

    def test_bin_error(self):
        cls = lib_mux.MP4Box()
        with self.assertRaises(subprocess.SubprocessError):
            cls._cmd = [sys.executable, "-c", "raise SystemExit(1)"]
            cls._test_bin_works()

    def test_bin_working(self):
        cls = lib_mux.MP4Box()
        cls.set_path(mp4boxbin)
        cls._test_bin()
        self.assertTrue(cls._tested)

    def test_bin_working_output(self):
        cls = lib_mux.MP4Box()
        cls.set_path(mp4boxbin)
        cls._test_bin()
        self.assertEqual(cls._bin_test_output, mp4box_output)

if __name__ == "__main__":
    unittest.main()
