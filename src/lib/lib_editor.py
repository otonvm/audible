#! python3
# -*- coding: utf-8 -*-

import textwrap
from config import Config

class Editor:
    def __init__(self, conf):
        if not isinstance(conf, Config):
            raise AssertionError("conf must be and instance of Config class.") from None

        self._conf = conf

        self._build_list()

        self._insert_line()

        number = 1
        for item in self._meta_list:
            self._print_info(number, title=item[0], text=item[1])
            number += 1

        self._insert_line()

    def _build_list(self):
        self._meta_list = [("Title", self._conf.title),
                           ("Authors", self._conf.authors),
                           ("Narrators", self._conf.narrators),
                           ("Series", self._conf.series_title),
                           ("Book Nº", self._conf.series_position),
                           ("Description", self._conf.description),
                           ("Copyright", self._conf.copyright)]

    def _insert_line(self, symbol='=', width=100):
        print(symbol * width)


    def _print_info(self, number, title, text, width=100):
        string = "{}) {}: {}".format(number, title, text)
        print(textwrap.fill(string, width=width))


if __name__ == "__main__":
    c = Config()
    c.title = "title"
    c.authors = ["ss", "dd"]
    e = Editor(c)

# import platform
#
# if platform.system() == 'Windows':
#     from msvcrt import getwch, putwch
# elif platform.system() == 'Darwin':
#     import lib.readline_mac.readline as readline
# else:
#     raise ImportError("Cannot import readline module on this system.") from None
#
#
# class InputWithText:
#     def __init__(self, prompt, default):
#         self._prompt = prompt
#         self._default = default
#
#         try:
#             _setup_win()
#         except ImportError:
#             #TODO: dummy function
#             pass
#
#     def __call__(self):
#         pass
#
#     def _setup_win(self):
#         from msvcrt import getwch, putwch
#
#     def _setup_mac(self):
#         import lib.readline_mac.readline as readline
#
# class _Widows:
#
# # def input_with_text(prompt, default):
# #     def pre_input_hook():
# #         readline.insert_text(default)
# #         #readline.redisplay()
# #
# #     readline.set_pre_input_hook(pre_input_hook)
# #     try:
# #         return input(prompt)
# #     finally:
# #         readline.set_pre_input_hook(None)
# #
# # if __name__ == "__main__":
# #     print(dir(readline))
# #     i = input_with_text("prompt:", "default")
# #     print(i)
# #
#
#
# def putstr(string):
#     for char in string:
#         putwch(char)
#
#
# def input_with_text(prompt, default=None):
#     putstr(prompt)
#
#     if default is None:
#         data = []
#     else:
#         data = list(default)
#         putstr(data)
#
#     while True:
#         char = getwch()
#
#         if char in '\r\n':
#             break
#         # Ctrl-C
#         elif char == '\003':
#             putstr('\r\n')
#             raise KeyboardInterrupt
#         # Backspace
#         elif char == '\b':
#             if data:
#                 # Backspace and wipe the character cell
#                 putstr('\b \b')
#                 data.pop()
#         # Special keys
#         elif char in '\0\xe0':
#             getwch()
#         else:
#             putwch(char)
#             data.append(char)
#
#     putstr('\r\n')
#
#     return ''.join(data)
#
# if __name__ == "__main__":
#     i = input_with_text("prompt:", "default")
#     print(i)
