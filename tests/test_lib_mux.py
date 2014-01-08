import unittest

import os
import sys
import subprocess
import platform

import lib.lib_mux as lib_mux


if platform.system() == "Windows":
    mp4boxbin = os.path.abspath(__file__)[:-22]
    mp4boxbin = os.path.join(mp4boxbin, "tools\win\mp4box.exe")
else:
    mp4boxbin = os.path.abspath(__file__)[:-22]
    mp4boxbin = os.path.join(mp4boxbin, "tools/mac/MP4Box")

class Test(unittest.TestCase):
    def test_bin_found(self):
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


if __name__ == "__main__":
    unittest.main()
