# CMediaSort Readme
## Short description
CMediaSort is a tool which sorts and downloads metadata for movies and episodes
based on their filename in a fully automated way.

It's the cli version for the MediaSort python library which itself is based
on the guessit library for guessing informations by analyzing the
file-/ foldername. It then uses this informations to scrape the metadata from
TMDb by using the tmdbsimple library. It's also able to download images via
TMDb or fanart.tv

This tool heavily depends on [TMDb](https://www.themoviedb.org/) for getting
informations and [fanart.tv](https://fanart.tv/) for getting images.
So please consider supporting these projects by contributing or donations.

This product uses the TMDb API but is not endorsed or certified by TMDb.

## Full description
CMediaSort currently sorts movies and episodes, but its written in a way
that more mediatypes can be supported very easy.

In the first step a guess must be taken so cmediasort knows what mediatype
we have. There are two methods which can be used to take a guess. Nfo, which
tries to open a nfo file besides the mediafile and searches for a imdb id.
The second method is by using the guessit library. With the guessit approach
it tries to guess the name, the source (blueray rip, dvdrip etc.) and the
releasegroup. For episodes it also guesses the episode and season number.

In the second step we try to get an exact ID for our mediafile. If we already
have the imdb id from the nfo, we use this id to get other ids like tmdb and
tvdb from tmdb.
If we only have the name, we will search tmdb for the name. TMDb is at the
moment the only supported id provider.

In the third step we download the metadata for this mediafile and use a
template engine to write it to a file. The template engine cmediasort uses
is mako. Scroll down to see an example template file. At the moment the
only supported metadata provider is TMDb.

In the last step we download several images for the media. As image provider
TMDb and fanart.tv is supported.

## Planned features
 - Add music and snes rom mediatype
 - Add Trailer download via youtube-dl
 - Add media information via mediainfo
 - Rewrite cmediasort in nim
 - Merge cmediasort and mediasort

## Note
I'm not that actively developping mediasort/cmediasort. But i'm using it by
myself, so i try to fix bugs, but i propably won't add more features until
I have more time for mediasort/cmediasort.

## Usage
```
cmediasort [-h] [-c CONFIG] [-i] [-v] [-a] [-s] source

Scrapes metadata for movies and episodes from TMDb by guessing the title from
scene standard naming conventions. This product uses the TMDb API but is not
endorsed or certified by TMDb.

positional arguments:
  source                The file or the folder which should be scanned for
                        files

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        the config file. Defaults to config.yaml in the
                        default config dir of your os.
  -i, --interactive     Asks the user if something is not clear
  -v, --verbose         Shows a lot more output
  -a, --ask             Asks before sorting
```

## A example config file
```
---

videofiles:
  minimal_file_size: 300
  allowed_extensions: ['mkv', 'avi']

tmdb:
  api_key: bd65f46c799046c2d4286966d76c37c6
  cache_validity: 7
  use_https: true
  certification_country: de
  sizes:
    poster: original
    background: original
    thumbnail: original

fanarttv:
  api_key: 975772e71680c85fc2944ca0492c691f

paths:
  movie:
    template: templates/movie/kodi-nfo-chris
    base: /mnt/chump/filme/${metadata['title']} (${metadata['premiered'][:4]})/
    nfo: ${metadata['title']} (${metadata['premiered'][:4]}).nfo
    media: ${metadata['title']} (${metadata['premiered'][:4]})
    poster: poster
    background: fanart
    disc: disc
    banner: banner
    logo: logo
    clearart: clearart
    art: art
  episode:
    template: templates/episode/kodi-nfo
    base: /mnt/chump/serien/${metadata['showtitle']} (${metadata['show_premiered'][:4]})/Staffel ${str(identificator['season']).zfill(2)}/
    nfo: S${str(identificator['season']).zfill(2)}E${str(identificator['episode']).zfill(2)} ${metadata['title']}.nfo
    media: S${str(identificator['season']).zfill(2)}E${str(identificator['episode']).zfill(2)} ${metadata['title']}
    thumbnail: S${str(identificator['season']).zfill(2)}E${str(identificator['episode']).zfill(2)} ${metadata['title']}-thumb
  season:
    base: /mnt/chump/serien/${metadata['showtitle']} (${metadata['show_premiered'][:4]})/
    poster: season${str(identificator['season']).zfill(2)}-poster
  tvshow:
    template: templates/tvshow/kodi-nfo
    base: /mnt/chump/serien/${metadata['showtitle']} (${metadata['show_premiered'][:4]})/
    nfo: tvshow.nfo
    poster: poster
    background: fanart
    banner: banner
    logo: logo
    charart: charart
    clearart: clearart
    art: art

overwrite:
  media: false
  nfo: true
  images: true

languages:
  metadata: ['de', 'en']
  images: ['de', 'en']

plugins:
  guess: ["nfo", "filename"]
  identificator:
    movie: ["nfo", "tmdb"]
    episode: ["nfo", "tmdb"]
  metadata:
    movie:
      title: ["tmdb"]
      originaltitle: ["tmdb"]
      set: ["tmdb"]
      premiered: ["tmdb"]
      tagline: ["tmdb"]
      plot: ["tmdb"]
      certification: ["tmdb"]
      rating: ["tmdb"]
      votes: ["tmdb"]
      studios: ["tmdb"]
      countries: ["tmdb"]
      genres: ["tmdb"]
      writers: ["tmdb"]
      directors: ["tmdb"]
      actors: ["tmdb"]
    tvshow:
      showtitle: ["tmdb"]
      premiered: ["tmdb"]
      plot: ["tmdb"]
      certification: ["tmdb"]
      rating: ["tmdb"]
      votes: ["tmdb"]
      studios: ["tmdb"]
      networks: ["tmdb"]
      genres: ["tmdb"]
      actors: ["tmdb"]
      creators: ["tmdb"]
    episode:
      showtitle: ["tmdb"]
      show_premiered: ["tmdb"]
      title: ["tmdb"]
      premiered: ["tmdb"]
      plot: ["tmdb"]
      rating: ["tmdb"]
      votes: ["tmdb"]
      actors: ["tmdb"]
      scriptwriters: ["tmdb"]
      certification: ["tmdb"]
      directors: ["tmdb"]
      studios: ["tmdb"]
      networks: ["tmdb"]
  images:
    movie:
      poster: ["tmdb", "fanarttv"]
      background: ["tmdb", "fanarttv"]
      disc: ["fanarttv"]
      banner: ["fanarttv"]
      logo: ["fanarttv"]
      clearart: ["fanarttv"]
      art: ["fanarttv"]
    tvshow:
      poster: ["tmdb", "fanarttv"]
      background: ["tmdb", "fanarttv"]
      banner: ["fanarttv"]
      logo: ["fanarttv"]
      clearart: ["fanarttv"]
      charart: ["fanarttv"]
      art: ["fanarttv"]
    season:
      poster: ["tmdb"]
    episode:
      thumbnail: ["tmdb"]

```

## Example template files
### Movie
```
<movie>
  % if metadata['title']:
	<title>${metadata['title']}</title>
  % endif
  % if metadata['originaltitle']:
	<originaltitle>${metadata['originaltitle']}</originaltitle>
  % endif
  % if metadata['premiered']:
	<year>${metadata['premiered']}</year>
  % endif
  % if metadata['tagline']:
	<tagline>${metadata['tagline']}</tagline>
  % endif
  % if metadata['plot']:
	<plot>${metadata['plot']}</plot>
  % endif
  % if metadata['set']:
	<set>${metadata['set']}</set>
  % endif
  % if metadata['certification']:
	<mpaa>${metadata['certification']}</mpaa>
  % endif
  % if metadata['rating']:
	<rating>${metadata['rating']}</rating>
  % endif
  % if metadata['votes']:
	<votes>${metadata['votes']}</votes>
  % endif
  % if metadata['studios']:
	  % for studio in metadata['studios']:
	<studio>${studio}</studio>
    % endfor
  % endif
  % if metadata['genres']:
	  % for genre in metadata['genres']:
	<genre>${genre}</genre>
    % endfor
  % endif
  % if metadata['directors']:
	  % for director in metadata['directors']:
	<director>${director}</director>
    % endfor
  % endif
  % if metadata['writers']:
	  % for writer in metadata['writers']:
	<credits>${writer}</credits>
    % endfor
  % endif
  % if metadata['actors']:
    % for actor in metadata['actors']:
	<actor>
		<name>${actor['name']}</name>
		<role>${actor['role']}</role>
	</actor>
    % endfor
  % endif
  % if identificator['imdb']:
	<id>${identificator['imdb']}</id>
  % endif
</movie>
```
### tvshow
```
<tvshow>
  % if metadata['showtitle']:
	<title>${metadata['showtitle']}</title>
  % endif
  % if metadata['rating']:
	<rating>${metadata['rating']}</rating>
  % endif
  % if metadata['votes']:
	<votes>${metadata['votes']}</votes>
  % endif
  % if metadata['premiered']:
	<premiered>${metadata['premiered']}</premiered>
  % endif
  % if metadata['plot']:
	<plot>${metadata['plot']}</plot>
  % endif
  % if metadata['certification']:
	<mpaa>${metadata['certification']}</mpaa>
  % endif
  % if identificator['imdb']:
	<id>${identificator['imdb']}</id>
  % endif
  % if metadata['studios']:
	% for studio in metadata['studios']:
	<studio>${studio}</studio>
    % endfor
  % endif
  % if metadata['genres']:
	% for genre in metadata['genres']:
	<genre>${genre}</genre>
    % endfor
  % endif
  % if metadata['actors']:
	  % for actor in metadata['actors']:
	<actor>
		<name>${actor['name']}</name>
		<role>${actor['role']}</role>
	</actor>
    % endfor
  % endif
</episodedetails>
```
### episode
```
<episodedetails>
  % if metadata['showtitle']:
	<showtitle>${metadata['showtitle']}</showtitle>
  % endif
  % if identificator['season']:
	<season>${identificator['season']}</season>
  % endif
  % if identificator['episode']:
	<episode>${identificator['episode']}</episode>
  % endif
  % if metadata['title']:
	<title>${metadata['title']}</title>
  % endif
  % if metadata['plot']:
	<plot>${metadata['plot']}</plot>
  % endif
  % if metadata['premiered']:
	<aired>${metadata['premiered']}</aired>
  % endif
  % if metadata['rating']:
	<rating>${metadata['rating']}</rating>
  % endif
  % if metadata['votes']:
	<votes>${metadata['votes']}</votes>
  % endif
  % if metadata['certification']:
	<votes>${metadata['certification']}</votes>
  % endif
  % if metadata['networks']:
    % for network in metadata['networks']:
	<studio>${network}</studio>
    % endfor
  % endif
  % if metadata['scriptwriters']:
    % for scriptwriter in metadata['scriptwriters']:
	<credits>${scriptwriter}</credits>
    % endfor
  % endif
  % if metadata['directors']:
	% for director in metadata['directors']:
	<director>${director}</director>
    % endfor
  % endif
  % if metadata['actors']:
	% for actor in metadata['actors']:
	<actor>
		<name>${actor['name']}</name>
		<role>${actor['role']}</role>
	</actor>
    % endfor
  % endif
</episodedetails>
```
