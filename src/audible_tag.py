#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.3"
__updated__ = "29.12.2013"

import os
import sys
import xml.etree.ElementTree as ET

try:
    import lib.lib_argparse as lib_argparse
    import lib.lib_audible as lib_audible
    import lib.lib_tree as lib_tree
    import lib.lib_exceptions as lib_exceptions
    import lib.lib_utils as lib_utils
    import config
except ImportError as err:
    print("Cannot start module {}".format(__file__), file=sys.stderr)
    print("Reason: {}".format(err.msg), file=sys.stderr)
    raise SystemExit(1)

DEBUG = 1


def setup_logging():
    if 'sys' not in locals().keys():
        import sys
    import inspect
    import logging

    try:
        import lib.lib_logger as lib_logger
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
        def set_log_level(*args): pass
        def ld(*args): pass
        def li(*args): pass
        def lw(*args): pass
        def le(*args): pass
        def lc(*args):
            raise SystemExit(1)


def parse_xml(conf):
    try:
        tree = ET.parse(conf.metadata_xml)
        root = tree.getroot()
        ld("root", root)
    except FileNotFoundError:
        lc("Could not open file: {}".format(conf.metadata_xml))
    except ET.ParseError as err:
        lc("Could not parse xml file: {}, error: {}".format(conf.metadata_xml, err.msg))

    for child in root:
        if child.tag == 'title':
            conf.title = child.text
        if child.tag == 'authors':
            for each in child:
                conf.authors.append(each.text)
        if child.tag == 'narrators':
            for each in child:
                conf.narrators.append(each.text)
        if child.tag == 'series':
            for each in child:
                if each.tag == 'title':
                    conf.series_title = each.text
                if each.tag == 'position':
                    conf.series_position = each.text
        if child.tag == 'runtime':
            conf.runtime = child.text
        if child.tag == 'description':
            conf.description = child.text
        if child.tag == 'copyright':
            conf.copyright = child.text

    if DEBUG:
        ld("conf.title", conf.title)
        ld("conf.authors", conf.authors)
        ld("conf.narrators", conf.narrators)
        ld("conf.series_title", conf.series_title)
        ld("conf.series_position", conf.series_position)
        ld("conf.runtime", conf.runtime)
        ld("conf.description", conf.description)
        ld("conf.copyright", conf.copyright)


def parse_url(conf):
    metadata = lib_audible.Metadata()

    try:
        metadata.http_page(conf.url)
    except lib_exceptions.URLException as err:
        lc(err.msg)
    except lib_exceptions.HTTPException as err:
        lc(err.msg)
    except lib_exceptions.BS4Exception as err:
        lc(err.msg)

    try:
        conf.title = metadata.title
    except lib_exceptions.RegExException as err:
        lw("Error parsing title. {}".format(err.msg))
        conf.title = metadata.title_raw
    ld("conf.title", conf.title)

    conf.authors = metadata.authors
    ld("conf.authors", conf.authors)

    conf.narrators = metadata.narrators
    ld("conf.narrators", conf.narrators)

    try:
        series = metadata.series()
    except lib_exceptions.RegExException as err:
        lw("Error parsing series. {}".format(err.msg))
        series = metadata.series(try_title=True)
    ld("series", series)

    if series:
        conf.series_title = series[0]
        conf.series_position = series[1]
    else:
        li("No series detected.")
        conf.series_title, conf.series_position = None, None
    ld("conf.series_title", conf.series_title)
    ld("conf.series_position", conf.series_position)

    try:
        conf.runtime = metadata.runtime_sec
    except lib_exceptions.RegExException as err:
        lw("Error parsing runtime. {}".format(err.msg))
        conf.runtime = metadata.runtime_string
    ld("conf.runtime", conf.runtime)

    conf.description = metadata.description
    ld("conf.description", conf.description)

    conf.copyright = metadata.copyright
    ld("conf.copyright", conf.copyright)


def write_xml(conf):
    root = ET.Element("audiobook")

    title = ET.SubElement(root, "title")
    title.text = conf.title

    authors = ET.SubElement(root, "authors")
    for author in conf.authors:
        name = ET.SubElement(authors, "name")
        name.text = author

    narrators = ET.SubElement(root, "narrators")
    for narrator in conf.narrators:
        name = ET.SubElement(narrators, "name")
        name.text = narrator

    series = ET.SubElement(root, "series")
    series_title = ET.SubElement(series, "title")
    series_title.text = conf.series_title
    series_position = ET.SubElement(series, "position")
    #BUG: ints must be converted to str!
    series_position.text = str(conf.series_position)

    runtime = ET.SubElement(root, "runtime")
    runtime.text = str(conf.runtime)

    description = ET.SubElement(root, "description")
    description.text = conf.description

    ab_copyright = ET.SubElement(root, "copyright")
    ab_copyright.text = conf.copyright

    tree = ET.ElementTree(root)

    tree.write(conf.metadata_xml, encoding="unicode", xml_declaration=True)


def main(argv):
    ld("argv", argv)

    program_version = "v{}".format(__version__)
    program_build_date = str(__updated__)
    program_version_message = "{}, built {}".format(program_version, program_build_date)

    args = lib_argparse.parser(program_version_message)
    ld(args)

    if args.verbose:
        set_log_level('debug')

    #initialize class to hold configuration:
    conf = config.Config()

    #parse arguments:
    #get folder contents:
    conf.input_folder = args.input_folder
    try:
        folder_contents = lib_tree.Parse(conf.input_folder)
        ld("folder_contents", folder_contents)
    except lib_exceptions.FolderNotFound as err:
        lc("Cannot find folder!")

    conf.audio_files = folder_contents.audio_files
    ld("conf.audio_files", conf.audio_files)

    conf.cover = folder_contents.cover
    ld("conf.cover", conf.cover)

    if not conf.cover:
        lw("No cover files specified or found. No artwork will be used.")

    #get metadata from either xml file or url:
    if args.input_xml:
        conf.metadata_xml = args.input_xml
        ld("conf.metadata_xml", conf.metadata_xml)
        parse_xml(conf)

    else:
        #default metadata.xml that could/should exist:
        conf.metadata_xml = os.path.join(args.input_folder, "metadata.xml")

        #check if an xml file already exists:
        if os.path.exists(conf.metadata_xml):
            li("A metadata.xml file found.")

            if lib_utils.yn_query("Would you like to use that?"):
                parse_xml(conf)

        #no xml files exist, parse url:
        #TODO: add a --force option
        else:
            conf.url = args.url
            ld("conf.url", conf.url)
            parse_url(conf)
            #write metadata to an xml file:
            write_xml(conf)


if __name__ == "__main__":
    if DEBUG:
        setup_logging()
        set_log_level('debug')
        sys.argv.append('-v')
        sys.argv.append('-i')
        sys.argv.append("/Users/Oton/Dropbox/Code/Eclipse_Mac/Audible/test_ab")
        sys.argv.append('-u')
        #sys.argv.append("http://www.audible.com/pd/Sci-Fi-Fantasy/The-Adversary-Audiobook/B00G3L6PZY/ref=a_series_c2_3_saTtl")
        sys.argv.append("http://www.audible.com/pd/Sci-Fi-Fantasy/A-Quest-of-Heroes-Audiobook/B00F9DZV3Y/ref=a_cat_Sci-F_c6_1_t")
        #sys.argv.append('-x')
        #sys.argv.append("/Users/Oton/Desktop/Audible/Audible/test_ab/meta.xml")
    else:
        setup_logging()
        set_log_level('error')

    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(1)

