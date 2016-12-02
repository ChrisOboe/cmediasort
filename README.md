# MediaSort Readme
MediaSort is a tool which sorts and downloads metadata for movies and episodes
based on their filename in a fully automated way.

It's written in python and uses the guessit library for guessing informations
based on filename / foldername.
It then uses this informations to scrape the metadata from TMDb by using the
tmdbsimple library.

This tool heavily depends on [TMDb](https://www.themoviedb.org/) for getting
informations and [fanart.tv](https://fanart.tv/) for getting images.
So please consider supporting these projects by contributing or donations.

This product uses the TMDb API but is not endorsed or certified by TMDb.

## Usage
```
mediasort [-h] [-v] [-c CONFIG] [-p] source
```

### Arguments
| short | long | description |
| -------- | -------- | -------- | 
| -h | --help | shows help |
| -v | --verbose | be more verbose |
| -c | --config | the configfile to use. Defaults to xdg_config_home/mediasort/config.ini |
| -t | --printconfig | prints the complete config file (with appended defaults) |

source: the path to the media files

### Important
Since this software is in a pretty early state configuration and command line
arguments can change often. So if you want how to use this program, take a look
into mediasortcli/config.py
