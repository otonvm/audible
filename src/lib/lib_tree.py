import os
import sys

class Parse:
    """
    Helper class for parsing a folder tree and getting out specific items.
    The tree_ in the name is there to help distinguish members of this class.

    tree_parse(folder): parses through a folder and creates a list of items in it
    tree_audio_files: property that returns a list of paths to audio files
    tree_cover: property that returns the path to a cover image
    tree_metadata: property that returns the path to a xml file that should contain
                   metadata information

    This class can be used directly or subclassed so that its members can be called
    from a child class. In that case two data members can also be overridden:
    audio_extensions: contains a list of supported extensions for audio files
    cover_extensions: contains a list of supported extensions for image files
    """

    def __init__(self, folder):
        self._folder = folder
        self._file_list = list()
        self._audio_files = list()
        self.audio_extensions = [".m4a", ".aac", ".m4b"]
        self._cover = str()
        self.cover_extensions = [".png", ".jpg", ".jpeg"]
        self._metadata_xml = str()

        self._parse()

    def _get_folder(self):
        folder = os.path.abspath(os.path.expanduser(self._folder))

        if not os.path.exists(folder):
            self._folder = None
        else:
            self._folder = folder

    def _glob_folder(self):
        for file in os.listdir(self._folder):
            self._file_list.append(file)

    def _get_audio_files(self):
        #create a new list of audio files if their extension is in a predefined list:
        self._audio_files = [os.path.abspath(file) for file in self._file_list
                             if os.path.splitext(file)[1] in self.audio_extensions]

    def _get_cover(self):
        #create a new list with all images:
        cover = [os.path.abspath(file) for file in self._file_list
                 if os.path.splitext(file)[1] in self.cover_extensions]

        #pick only the first image if there are more then one:
        if len(cover) > 1:
            self._cover = cover[0]
        else:
            try:
                self._cover = cover[0]
            except IndexError:
                self._cover = None

    def _get_metadata_xml(self):
        #create a new list with all xml files:
        xml_files = [os.path.abspath(file) for file in self._file_list
                     if os.path.splitext(file)[1] == ".xml"]

        if len(xml_files) > 1:
            self._metadata_xml = xml_files[0]
        else:
            try:
                self._metadata_xml = xml_files[0]
            except IndexError:
                self._metadata_xml = None

    def _parse(self):
        self._get_folder()

        if self._folder:
            self._glob_folder()
            #sort the list of files alphabetically:
            self._file_list.sort()
        else:
            raise IOError("Cannot find folder!") from None

    @property
    def audio_files(self):
        self._get_audio_files()
        return self._audio_files

    @property
    def cover(self):
        self._get_cover()
        return self._cover

    @property
    def metadata(self):
        self._get_metadata_xml()
        return self._metadata_xml
