#! python3
# -*- coding: utf-8 -*-

"""
Copy the following into a script. Make sure it can import lib_logger module.

Initialize with:
setup_logging()

Then short functions can be used for logging:
    ld(text) -> debug with "text"
    ld(label, text) -> debug with "label: text"
    ld(label, text1, text2, text*) -> debug with "label: text1, text2, ..."
    li(text) -> info "text"
    lw(text) -> warning "text"
    le(text) -> error "text" [does NOT exit]
    lc(text) -> critical "text" [raises SystemExit]

Logging level can be set with:
    set_log_level(level)

level defaults to 'error'.
"""

#COPY THE FOLLOWING:
def setup_logging():
    import sys
    import inspect
    import logging

    try:
        import lib_logger
        enabled = True
    except ImportError as err:
        print("Cannot import logger module because: {}. Logging disabled.".format(err.msg), file=sys.stderr)
        enabled = False

    #set global names:
    global set_log_level
    global ld
    global li
    global lw
    global le
    global lc

    if enabled:
        #connect to logger from logger module:
        logger = logging.getLogger('logger')

        def set_log_level(level='error'):
            lib_logger.set_log_level(level)

        set_log_level()

        #define shorthand function for debug:
        def ld(label='', *args):
            #get the real line number of where this message originated:
            lineno = str(inspect.getframeinfo(inspect.currentframe().f_back)[1])
            if len(args) == 0:
                logger.debug(label, extra={'true_lineno': lineno})
            elif len(args) == 1:
                msg = args[0]
                logger.debug("{}: {}".format(label, msg), extra={'true_lineno': lineno})
            else:
                msg = ', '.join([arg for arg in args])
                logger.debug("{}: {}".format(label, msg), extra={'true_lineno': lineno})

        #define shorthand function for info:
        li = logger.info

        #define shorthand function for warning:
        lw = logger.warning

        #define shorthand function for error:
        def le(msg):
            lineno = str(inspect.getframeinfo(inspect.currentframe().f_back)[1])
            #get the real line function name of where this message originated:
            func = inspect.getframeinfo(inspect.currentframe().f_back)[2]
            logger.error(msg, extra={'true_lineno': lineno, 'true_func': func})

        #define shorthand function for critical error:
        def lc(msg):
            lineno = str(inspect.getframeinfo(inspect.currentframe().f_back)[1])
            func = inspect.getframeinfo(inspect.currentframe().f_back)[2]
            logger.critical(msg, extra={'true_lineno': lineno, 'true_func': func})
            raise SystemExit(1)

    else:
        #define backup shorthand functions:
        def ld(*args): pass
        def li(*args): pass
        def lw(*args): pass
        def le(*args): pass
        def lc(*args):
            raise SystemExit(1)

#END COPY

import sys
import logging

class CustomStreamHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.stream = None #reset the default logging stream

    def _custom_emit(self, record, stream):
        """Private function that calls the parent emit function."""
        self.stream = stream
        logging.StreamHandler.emit(self, record)

    def emit(self, record):
        #everything above and including ERROR goes to stderr
        if record.levelno >= logging.ERROR:
            self._custom_emit(record, sys.stderr)
        elif record.levelno == logging.DEBUG:
            self.stream = sys.stdout
            logging.StreamHandler.emit(self, record)
            with open('debug.log', mode='w', encoding='utf-8') as log:
                self.stream = log
                logging.StreamHandler.emit(self, record)
        else: #everything below goes to stdout
            self._custom_emit(record, sys.stdout)


class CustomFormatter(logging.Formatter):
    #'{' = using StrFormatStyle (str.format())
    #inside {} are usual logging parameters
    _FORMATS = {
                logging.DEBUG   : logging._STYLES['{']("file: {filename} | DEBUG, line {true_lineno}: {message}"),
                logging.INFO    : logging._STYLES['{']("{asctime} | {message}"),
                logging.WARNING : logging._STYLES['{']("{levelname}: {message}"),
                logging.ERROR   : logging._STYLES['{']("{asctime} | file: {filename} | {levelname} in {true_func}({true_lineno}): {message}"),
                logging.CRITICAL: logging._STYLES['{']("{asctime} | file: {filename} | {levelname} in {true_func}({true_lineno}): {message}"),
                'DEFAULT'       : logging._STYLES['{']("{module}: {message}")
                }

    def __init__(self):
        #call parent __init__ and set datefmt:
        logging.Formatter.__init__(self, datefmt="%m/%d/%Y %H:%M:%S")
        self._style = None #reset default _style

    def format(self, record):
        #set _style to one from _FORMATS or DEFAULT:
        self._style = self._FORMATS.get(record.levelno, self._FORMATS['DEFAULT'])
        return logging.Formatter.format(self, record)

logger = logging.getLogger('logger')
handler = CustomStreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.propagate = False

def set_log_level(level):
    if level not in ['debug', 'info', 'warning', 'error', 'critical']:
        print("Valid logging levels are: 'debug', 'info', 'warning', 'error' or 'critical'!")
        logger.setLevel(logging.DEBUG)
    elif level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif level == 'info':
        logger.setLevel(logging.INFO)
    elif level == 'warning':
        logger.setLevel(logging.WARNING)
    elif level == 'error':
        logger.setLevel(logging.ERROR)
    elif level == 'critical':
        logger.setLevel(logging.CRITICAL)

