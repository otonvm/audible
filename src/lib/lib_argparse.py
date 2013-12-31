#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

def parser(version):
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_false',
                        help="Display verbose information. [default: %(default)s]")
    parser.add_argument('-i', '--input', dest='input_folder', metavar='<folder path>', action='store',
                        help="Input folder that contains all items.", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-x', '--xml', dest='input_xml', metavar='<xml path>', action='store',
                        help="Path to XML file with metadata information. [default: None]")
    group.add_argument('-u', '--url', dest='url', metavar='<URL>', action='store',
                        help="URL to audible page with metadata [default: None]")

    parser.add_argument('-c', '--cover', dest='input_cover', metavar='<cover image path>', action='store',
                        help="Path to a cover image. [default: None]")
    parser.add_argument('-V', '--version', action='version', version=version)

    args = parser.parse_args()

    return args

