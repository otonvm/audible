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

    def tag(self, data):
        if not isinstance(data, dict):
            raise TypeError("metadata must be a dict")

        def cmd_append(arg1, arg2):
            self._cmd.append(arg1)
            try:
                self._cmd.append(data[arg2])
            except KeyError:
                self._cmd.append("")

        file_path, file_name = os.path.split(data["file"])
        file_name = os.path.splitext(file_name)[0]

        file = "{}_final.m4b".format(os.path.join(file_path, file_name))

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
        cmd_append("--artwork", "cover")
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

        print(self._cmd)
