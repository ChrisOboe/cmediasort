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
import os
import argparse
import yaml
from appdirs import user_config_dir

import mediasort

PROG = "cmediasort"


def parse_arguments():
    """Returns a dict of command line arguments."""

    parser = argparse.ArgumentParser(
        prog=PROG,
        description='Scrapes metadata for movies and episodes from TMDb '
        'by guessing the title from scene standard naming conventions.\n'
        'This product uses the TMDb API but is not endorsed or certified '
        'by TMDb.')
    parser.add_argument(
        "source",
        help="The file or the folder which should be scanned for files ")
    parser.add_argument(
        '-c',
        '--config',
        default="{0}/config.yaml".format(user_config_dir(PROG)),
        help="the config file")
    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        help="Asks the user if something is not clear")

    return vars(parser.parse_args())


def parse_configfile(path):
    """Returns a dict of settings."""

    if os.path.isfile(path):
        stream = open(path, 'r')
        userconfig = yaml.load(stream)
    else:
        userconfig = {}
    return userconfig


def find(path, extensions, filesize):
    """ returns all files with given extensions
    and bigger than filesize in path """

    filesize *= 1048576  # use filesize as MB
    if not os.path.exists(path):
        return

    mediafiles = []
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lower()[1:]
        if ext in extensions and os.path.getsize(path) >= filesize:
            mediafiles.append(path)
    else:
        for root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                ext = os.path.splitext(filename)[1].lower()[1:]
                if (ext not in extensions) or \
                   (os.path.getsize(filepath) < filesize):
                    continue
                mediafiles.append(filepath)

    return mediafiles


def identificator_callback(identificator_list, medianame):
    """ the identificator callback function for interactive mode """
    c = 1
    for entry in identificator_list:
        print("{0}: {1}".format(c, entry['title']))
        c = c + 1
    selection = -1
    while selection < 1 or selection >= c:
        try:
            selection = int(input("Select your {0}: ".format(medianame)))
        except ValueError:
            pass
    selection = selection - 1
    return identificator_list[selection]['id']


def main():
    """ Main function for entry point """
    # load config
    args = parse_arguments()
    settings = parse_configfile(args['config'])

    # modify settings
    for mediatype in settings['paths']:
        if 'template' not in settings['paths'][mediatype]:
            continue

        template = settings['paths'][mediatype]['template']
        if not template.startswith("/"):
            settings['paths'][mediatype]['template'] = "{0}/{1}".format(
                user_config_dir(PROG),
                template
            )

    callbacks = {
        'identificator': None
    }

    if args['interactive']:
        callbacks['identificator'] = identificator_callback


    # get list of files
    videofiles = find(
        args['source'],
        settings['videofiles']['allowed_extensions'],
        settings['videofiles']['minimal_file_size'])

    if not videofiles:
        print("No videofile(s) found!")
        sys.exit(0)

    init = mediasort.initialize_plugins(settings)
    plugins = init['plugins']
    ids = init['ids']
    for videofile in videofiles:
        mediasort.sort(videofile,
                       plugins,
                       ids,
                       settings['paths'],
                       settings['languages'],
                       settings['overwrite'],
                       callbacks=callbacks)


if __name__ == '__main__':
    main()
