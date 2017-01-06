#!/usr/bin/env python3
# Copyright (C) 2016  Oboe, Chris <chrisoboe@eml.cc>
# Author: Oboe, Chris <chrisoboe@eml.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" the executable for mediasort """

import sys
import logging
import mediasort
from . import config


def verbose():
    """ logs info to stdout """
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.handlers = []
    logout = logging.StreamHandler(sys.stdout)
    logout.setLevel(logging.INFO)
    log.addHandler(logout)


def print_config(config):
    """ prints the configuration """
    for entry in config:
        print("[" + entry + "]")
        for subentry in config[entry]:
            if isinstance(config[entry][subentry], list):
                print(subentry + "=" + ' '.join(config[entry][subentry]))
            else:
                print(subentry + "=" + str(config[entry][subentry]))
        print("")


def main():
    """ Main function for entry point """
    # load config
    args = config.parse_arguments()
    settings = config.parse_configfile(args['config'])

    mediasort.tmdb.init(settings['tmdb'])
    mediasort.fanarttv.init(settings['fanarttv'])

    # init stuff
    logging.getLogger("requests").setLevel(logging.WARNING)
    if args['verbose']:
        verbose()

    if args['printconfig']:
        print_config(settings)
        return()

    # get list of files
    videofiles = mediasort.helpers.find(
        args['source'],
        settings['videofiles']['allowed_extensions'],
        settings['videofiles']['minimal_file_size'])

    for videofile in videofiles:
        mediasort.sort(videofile, settings)


if __name__ == '__main__':
    main()
