#! python3
# -*- coding: utf-8 -*-

import os
import subprocess


class MP4Box:
    def __init__(self):
        self._mp4box = str()
        self._cmd = list()
        self._bin_test_output = str()
        self._tested = False

    def set_path(self, path):
        self._mp4box = path

    def _test_bin_exists(self):
        try:
            if not os.path.exists(self._mp4box):
                raise FileNotFoundError("MP4Box binary not found") from None
        except TypeError:
            raise FileNotFoundError("MP4Box binary not found") from None
        return

    def _test_bin_works(self):
        with subprocess.Popen(self._cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as popen:
            try:
                _, self._bin_test_output = popen.communicate(timeout=2)
                retcode = popen.returncode

                if retcode != 0:
                    raise subprocess.SubprocessError("Error running MP4Box: <code {}>".format(retcode)) from None
            except subprocess.TimeoutExpired:
                popen.kill()
                popen.wait()
                raise subprocess.SubprocessError("Error running MP4Box: <timeout>") from None
        return

    def _test_bin(self):
        self._test_bin_exists()
        self._cmd = [self._mp4box, "-h", "general"]
        self._test_bin_works()
        self._tested = True
        return
