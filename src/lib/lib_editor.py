import platform

if platform.system() == 'Windows':
    from msvcrt import getwch, putwch
elif platform.system() == 'Darwin':
    import lib.readline_mac.readline as readline
else:
    raise ImportError("Cannot import readline module on this system.") from None


# def input_with_text(prompt, default):
#     def pre_input_hook():
#         readline.insert_text(default)
#         #readline.redisplay()
#
#     readline.set_pre_input_hook(pre_input_hook)
#     try:
#         return input(prompt)
#     finally:
#         readline.set_pre_input_hook(None)
#
# if __name__ == "__main__":
#     print(dir(readline))
#     i = input_with_text("prompt:", "default")
#     print(i)
#


def putstr(string):
    for char in string:
        putwch(char)


def input_with_text(prompt, default=None):
    putstr(prompt)

    if default is None:
        data = []
    else:
        data = list(default)
        putstr(data)

    while True:
        char = getwch()

        if char in '\r\n':
            break
        # Ctrl-C
        elif char == '\003':
            putstr('\r\n')
            raise KeyboardInterrupt
        # Backspace
        elif char == '\b':
            if data:
                # Backspace and wipe the character cell
                putstr('\b \b')
                data.pop()
        # Special keys
        elif char in '\0\xe0':
            getwch()
        else:
            putwch(char)
            data.append(char)

    putstr('\r\n')

    return ''.join(data)

if __name__ == "__main__":
    i = input_with_text("prompt:", "default")
    print(i)
