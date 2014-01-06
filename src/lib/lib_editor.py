#! python3
# -*- coding: utf-8 -*-

import textwrap
import lib.lib_utils as lib_utils
from config import Config

class Editor:
    def __init__(self, conf):
        if not isinstance(conf, Config):
            raise AssertionError("conf must be and instance of Config class.") from None

        self._conf = conf
        self._meta_list = list()

        #create a list of tuples with entries to edit:
        self._build_list()

        #clear the screen:
        if not conf.debug:
            lib_utils.clear()

        self._insert_line()

        #number to use for selection and display
        number = 1
        for item in self._meta_list:
            #print entries to screen:
            self._print_info(number, title=item[0], text=item[1])
            number += 1

        self._insert_line()

        number -= 1
        while True:
            if lib_utils.yn_query("Do you wish to edit an entry?"):
                selection = self._prompt(number)

                self._edit(selection)
            else:
                break

    def _build_list(self):
        #extract authors from list and create a readable string:
        authors = self._conf.authors
        authors_string = ', '.join([author for author in authors])

        #same for narrators:
        narrators = self._conf.narrators
        narrators_string = ', '.join([narrator for narrator in narrators])

        self._meta_list = [("Title", self._conf.title),
                           ("Authors", authors_string),
                           ("Narrators", narrators_string),
                           ("Series", self._conf.series_title),
                           ("Book Nº", self._conf.series_position),
                           ("Description", self._conf.description),
                           ("Copyright", self._conf.copyright)]

    def _insert_line(self, symbol='=', width=100):
        print(symbol * width)

    def _print_info(self, number, title, text, width=100):
        string = "{}) {}: {}".format(number, title, text)
        print(textwrap.fill(string, width=width))

    def _prompt(self, number):
        while True:
            answer = input("Enter a number from 1-{} to edit that entry: ".format(number))

            try:
                answer = int(answer)

                if answer <= number:
                    return answer
                else:
                    continue
            except ValueError:
                continue

    def _edit(self, number):
        def get_edit(number):
            return input("{}: ".format(self._meta_list[number-1][0]))

        if number == 1:
            title = get_edit(1)
            self._conf.title = title

        if number == 2:
            authors_string = get_edit(2)
            authors_list = authors_string.split(sep=', ')

            self._conf.authors = authors_list

        if number == 3:
            narrators_string = get_edit(3)
            narrators_list = narrators_string.split(sep=', ')

            self._conf.narrators = narrators_list

        if number == 4:
            series_title = get_edit(4)
            self._conf.series_title = series_title

        if number == 5:
            series_position = get_edit(5)
            self._conf.series_position = series_position

        if number == 6:
            description = get_edit(6)
            self._conf.description = description

        if number == 7:
            copyright = get_edit(7)
            self._conf.copyright = copyright

