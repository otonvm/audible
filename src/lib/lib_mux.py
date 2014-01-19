#! python3
# -*- coding: utf-8 -*-

import os
import subprocess
import platform
import lib.lib_exceptions as lib_exceptions
import lib.progress as progress


class MP4Box:

    def __init__(self, path_to_mp4box):
        self._mp4box = path_to_mp4box

        self._cmd = list()
        self._bin_test_output = str()
        self._tested = False

        self._file_name = str()
        self._file_path = str()
        self._aac_file = str()
        self._m4b_file = str()

        self._progress_bar = None

    def _test_bin_exists(self):
        try:
            if not os.path.exists(self._mp4box):
                raise FileNotFoundError("MP4Box binary not found") from None
        except:
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

    def _delete(self, file):
        try:
            os.remove(file)
        except OSError:
            pass

    def _progress_bar_init(self, width=80):
        self._progress_bar = progress.ProgressBar(total_width=width)

    def _progress_bar_update(self, percentage):
        if not self._progress_bar:
            self._progress_bar_init()

        self._progress_bar.update_amount(percentage)
        self._progress_bar.draw()

    def _demux(self, file, display_progress, bar_width):
        if not self._tested:
            self._test_bin()

        if platform.system() == "Windows":
            start_index = 15
            stop_index = 17
        else:
            start_index = 14
            stop_index = 16


        self._delete(self._aac_file)

        self._cmd = [self._mp4box, "-raw", "1", file, "-out", self._aac_file]

        try:
            proc = subprocess.Popen(self._cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            if display_progress:
                print()
                print("Demux:")
                print("-" * bar_width)
                self._progress_bar_init(width=bar_width)

                while proc.poll() != 0:
                    line = proc.stderr.read(46).decode('utf-8')

                    if line:
                        if "Error" in line:
                            output = proc.stderr.readline().decode('utf-8').strip()
                            error = output.split(': ')[1]
                            raise lib_exceptions.MP4BoxError(error)

                        try:
                            number = int(line[start_index:stop_index])
                            if number >= 0:
                                self._progress_bar_update(number)
                            else:
                                self._progress_bar_update(0)
                        except ValueError:
                            pass
                    else:
                        self._progress_bar_update(100)
                return proc.poll()
            else:
                output = proc.communicate()[1].decode('utf-8').strip()
                if "Error" in output:
                    error = output.split(': ')[1]
                    raise lib_exceptions.MP4BoxError(error)
                return proc.poll()
        except:
            raise

    def _remux(self, part_no, display_progress, bar_width):
        if platform.system() == "Windows":
            start_index = 10
            stop_index = 12
        else:
            start_index = 9
            stop_index = 11

        self._delete(self._m4b_file)

        self._cmd = [self._mp4box, "-brand", "M4B ", "-ab", "mp71", "-ipod", "-add",
                     "{}:name=Part {}:lang=eng".format(self._aac_file, part_no), self._m4b_file]

        try:
            proc = subprocess.Popen(self._cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            if display_progress:
                self._progress_bar = None
                self._progress_bar_init(width=bar_width)
                print()
                print("Remuxing file:")
                print("-" * bar_width)

                imported = False
                while not imported and proc.poll() != 0:
                    line = proc.stderr.read(47).decode('utf-8')

                    if line:
                        if "Error" in line:
                            output = proc.stderr.readline().decode('utf-8').strip()
                            error = output.split(': ')[1]
                            raise lib_exceptions.MP4BoxError(error)

                        try:
                            number = int(line[start_index:stop_index])
                            if number >= 0 and number < 95:
                                self._progress_bar_update(number)
                            #hack for ignoring remuxing phase
                            #it's usually so fast that it doesn't really matter
                            elif number >= 95:
                                self._progress_bar_update(100)
                                imported = True  # break the while loop
                            else:
                                self._progress_bar_update(0)
                        except ValueError:
                            pass
                    else:
                        self._progress_bar_update(100)
                proc.communicate()  # needed to deblock the process
                return proc.wait()
            else:
                output = proc.communicate()[1].decode('utf-8').strip()
                if "Error" in output:
                    error = output.split(': ')[1]
                    raise lib_exceptions.MP4BoxError(error)
                return proc.wait()
        except:
            raise

    def remux(self, file, part_no=1, display_progress=True, bar_width=80):
        self._file_path, self._file_name = os.path.split(file)
        self._file_name = os.path.splitext(self._file_name)[0]

        self._aac_file = r"{}_demux.aac".format(os.path.join(self._file_path, self._file_name))
        self._m4b_file = r"{}_temp.m4b".format(os.path.join(self._file_path, self._file_name))

        if not isinstance(part_no, int):
            raise TypeError("part_no must be of type int")
        if not isinstance(display_progress, bool):
            raise TypeError("display_progress must be of type bool")
        if not isinstance(bar_width, int):
            raise TypeError("bar_width must be of type int")

        if self._demux(file, display_progress, bar_width) == 0:
            if self._remux(part_no, display_progress, bar_width) == 0:
                self._delete(self._aac_file)
                return True
            else:
                self._delete(self._aac_file)
                self._delete(self._m4b_file)
                return False
        else:
            self._delete(self._aac_file)
            self._delete(self._m4b_file)
            return False
