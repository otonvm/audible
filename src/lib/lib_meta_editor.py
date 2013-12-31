import platform

if platform.system() == 'Windows':
    import lib.readline_win.readline as readline
elif platform.system() == 'Darwin':
    import lib.readline_mac.readline as readline
else:
    raise ImportError("Cannot import readline module on this system.") from None

def input_with_text(prompt, default):
    def pre_input_hook():
        readline.insert_text(default)
        readline.redisplay()

    readline.set_pre_input_hook(pre_input_hook)
    try:
        return input(prompt)
    finally:
        readline.set_pre_input_hook(None)
