#! python3
# -*- coding: utf-8 -*-

import os
import subprocess
import lib.lib_exceptions as lib_exceptions


class APTagger:

    def __init__(self, path_to_ap):
        self._ap = path_to_ap

        self._bin_test_output = str()
        self._tested = False

        self._metadata = dict()
        self._cmd = list()

    def _test_bin(self):
        try:
            with subprocess.Popen(self._ap, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                try:
                    self._bin_test_output, _ = proc.communicate(timeout=2)

                    retcode = proc.returncode
                    if retcode != 0:
                        raise subprocess.SubprocessError("Error running AtomicParsley: <code {}>".format(retcode)) from None
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                    raise subprocess.SubprocessError("Error running AtomicParsley: <timeout>") from None

        except FileNotFoundError:
            raise lib_exceptions.APError("AtomicParsley binary not found") from None

        self._tested = True
        return

    def _delete(self, file):
        try:
            os.remove(file)
        except OSError:
            pass

    def _ap_tag(self):
        if not self._tested:
            self._test_bin()

        os.environ["PIC_OPTIONS"] = "MaxDimensions=0:MaxKBytes=0:removeTempPix"
        
        try:
            with subprocess.Popen(self._cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
                stdout, _ = proc.communicate()
                stdout = stdout.decode('utf-8')

                if "error" in stdout:
                    err_line = stdout.split(': ')[1]
                    err = err_line.split('\n')[0].strip()
                    raise lib_exceptions.APError(err)

                retcode = proc.wait()
                if retcode == 0:
                    return True
                else:
                    return False
        except TypeError:
            raise lib_exceptions.APError("wrong type used for arg")

    def tag(self, data, display_progress=True, bar_width=80):
        if not isinstance(data, dict):
            raise TypeError("metadata must be a dict")
        
        def cmd_append(arg1, arg2):
            self._cmd.append(arg1)
            try:
                if data[arg2] is None:
                    raise KeyError
                self._cmd.append(str(data[arg2]))
            except KeyError:
                self._cmd.append("")

        file_path, file_name = os.path.split(data["file"])
        file_name = os.path.splitext(file_name)[0]

        file = r"{}_temp.m4b".format(os.path.join(file_path, file_name))
        final_file = r"{}.m4b".format(os.path.join(file_path, file_name))
        
        self._cmd.append(self._ap)
        self._cmd.append(file)
        cmd_append("--artist", "artist")
        cmd_append("--albumArtist", "album_artist")
        cmd_append("--title", "title")
        self._cmd.append("--sortOrder")
        cmd_append("name", "sort_title")
        cmd_append("--album", "album")
        self._cmd.append("--tracknum")
        self._cmd.append("{}/{}".format(data["track_no"], data["total_no"]))
        cmd_append("--disk", "disk_no")
        cmd_append("--year", "year")
        cmd_append("--copyright", "copyright")
        cmd_append("--ISO-copyright", "copyright")
        cmd_append("--description", "description")
        cmd_append("--longdesc", "description")
        cmd_append("--storedesc", "description")
        if data["cover"]:
            self._cmd.append("--artwork")
            self._cmd.append(data["cover"])
        self._cmd.append("--genre")
        self._cmd.append("Audiobooks")
        self._cmd.append("--stik")
        self._cmd.append("Audiobook")
        cmd_append("--comment", "empty")
        cmd_append("--composer", "empty")
        self._cmd.append("--purchaseDate")
        self._cmd.append("timestamp")
        cmd_append("--encodingTool", "empty")
        cmd_append("--encodedBy", "empty")
        self._cmd.append("--output")
        self._cmd.append(final_file)

        self._delete(final_file)

        print()
        print("Tagging...")

        if self._ap_tag():
            self._delete(file)
            return True
        else:
            self._delete(final_file)
            return False

