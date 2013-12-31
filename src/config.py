#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Config:
    def __init__(self):
        self._input_folder = str()
        self._audio_files = list()
        self._cover = str()

        self._metadata_xml = str()
        self._url = str()

        self._title = str()
        self._authors = list()
        self._narrators = list()
        self._series_title = str()
        self._series_position = int()
        self._runtime = int()
        self._description = str()
        self._copyright = str()

    @property
    def input_folder(self):
        return self._input_folder

    @input_folder.setter
    def input_folder(self, val):
        self._input_folder = val

    @property
    def audio_files(self):
        return self._audio_files

    @audio_files.setter
    def audio_files(self, val):
        self._audio_files.append(val)

    @property
    def cover(self):
        return self._cover

    @cover.setter
    def cover(self, val):
        self._cover = val

    @property
    def metadata_xml(self):
        return self._metadata_xml

    @metadata_xml.setter
    def metadata_xml(self, val):
        self._metadata_xml = val

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        self._url = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, val):
        self._authors.append(val)

    @property
    def narrators(self):
        return self._narrators

    @narrators.setter
    def narrators(self, val):
        self._narrators.append(val)

    @property
    def series_title(self):
        return self._series_title

    @series_title.setter
    def series_title(self, val):
        self._series_title = val

    @property
    def series_position(self):
        return self._series_position

    @series_position.setter
    def series_position(self, val):
        self._series_position = val

    @property
    def runtime(self):
        return self._runtime

    @runtime.setter
    def runtime(self, val):
        self._runtime = val

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val

    @property
    def copyright(self):
        return self._copyright

    @copyright.setter
    def copyright(self, val):
        self._copyright = val

