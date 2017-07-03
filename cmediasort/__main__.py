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
import logging
from appdirs import user_config_dir

import mediasort


PROG = "cmediasort"
ARGS = None


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
        help="the config file. Defaults to config.yaml in the default"
        "config dir of your os.")
    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        help="Asks the user if something is not clear")
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help="Shows a lot more output")
    parser.add_argument(
        '-a',
        '--ask',
        action='store_true',
        help="Asks before sorting")

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
    if len(identificator_list) > 1:
        c = 1
        for entry in identificator_list:
            print("{0}: {1}".format(c, entry['title']))
            c = c + 1
        print("i: Ignore this {0}".format(medianame))
        selection = -1
        while selection < 0 or selection >= c-1:
            print("Select your {0}: ".format(medianame), end='')
            sys.stdout.flush()
            sys.stdin.flush()
            choice = sys.stdin.readline().rstrip()
            if choice == "i":
                raise mediasort.error.CallbackBreak()
            else:
                try:
                    selection = int(choice)
                    selection = selection - 1
                except ValueError:
                    pass
        return identificator_list[selection]['id']
    else:
        if not ARGS['ask']:
            return identificator_list[0]['id']
        else:
            while True:
                print("Is {0} your {1}? [Yes/no] ".format(
                    identificator_list[0]['title'],
                    medianame), end=''
                )
                sys.stdout.flush()
                sys.stdin.flush()
                choice = sys.stdin.readline().lower().rstrip()
                if choice == "yes" or choice == "":
                    return identificator_list[0]['id']
                elif choice == "no":
                    raise mediasort.error.CallbackBreak()
                else:
                    print("Didn't understood your response")


def init_logging(debug):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('mediasort')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    format = '%(message)s'
    console = logging.StreamHandler()
    if debug:
        logger.setLevel(logging.DEBUG)
        format = '%(levelname)s: %(message)s'
    console.setFormatter(logging.Formatter(format))
    logger.addHandler(console)


def main():
    """ Main function for entry point """
    # load config
    global ARGS
    ARGS = parse_arguments()
    settings = parse_configfile(ARGS['config'])

    init_logging(ARGS['verbose'])

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

    if ARGS['interactive'] or ARGS['ask']:
        print("Running in interactive mode")
        callbacks['identificator'] = identificator_callback

    # get list of files
    videofiles = find(
        ARGS['source'],
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
    try:
        main()
    except KeyboardInterrupt:
        exit()
