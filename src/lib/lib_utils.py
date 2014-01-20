#! python3
# -*- coding: utf-8 -*-

import os
import pickle
import platform


def get_input(message):
    return input(message).strip().lower()


def yn_query(message):
    while True:
        answer = get_input("{} [Y/n] ".format(message))
        if answer == 'y' or len(answer) == 0:
            answer = True
            break
        elif answer == 'n':
            answer = False
            break
        else:
            continue
    return answer


def clear():
    if platform.system() == 'Windows':
        os.system("cls")
    elif platform.system() == 'Darwin':
        os.system("clear")


def load_pickle(path):
    try:
        with open(path, mode='rb') as file:
            return pickle.load(file, encoding='utf-8')
    except (pickle.UnpicklingError, OSError):
        return None


def dump_pickle(path, obj):
    try:
        with open(path, mode='wb') as file:
            pickle.dump(obj, file)
            return True
    except (pickle.PicklingError, OSError):
        return False
