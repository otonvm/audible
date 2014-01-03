#! python3
# -*- coding: utf-8 -*-


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
