#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'David Farrell'
SITENAME = 'Nosferalatu'
SITEURL = 'https://nosferalatu.com'
CUSTOM_LICENSE='Content licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC-BY-4.0</a>'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/nosferalatu'),
          ('github', 'http://github.com/nosferalatu'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

OUTPUT_PATH = '../site'

# MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra']

DISPLAY_PAGES_ON_MENU = True

THEME = 'themes/pelican-bootstrap3'
#THEME = 'themes/tuxlite_tbs'
#THEME = 'themes/pelican-simplegrey'
#THEME = 'themes/modernscientist'
#THEME = 'themes/nosferalatu'

#BOOTSTRAP_THEME = 'flatly'
#BOOTSTRAP_THEME = 'slate'
#BOOTSTRAP_THEME = 'spacelab'
#BOOTSTRAP_THEME = 'cyborg'
BOOTSTRAP_THEME = 'yeti'

#PYGMENTS_STYLE = 'solarizeddark'
#PYGMENTS_STYLE = 'solarizedlight'
PYGMENTS_STYLE = 'emacs'
#PYGMENTS_STYLE = 'autumn'
#PYGMENTS_STYLE = 'monokai'

# We put our theme customizations into our own custom.css file
# Pelican needs path separators to be OS-specific (e.g. backslash for Windows)
CUSTOM_CSS = 'static/custom.css'

# Tell Pelican what to add to the output dir
STATIC_PATHS = ['images', 'extra\custom.css', 'CNAME', 'js', 'raw']

# Tell Pelican to change the path to 'static/custom.css' in the output dir
EXTRA_PATH_METADATA = {
    'extra\custom.css': {'path': 'static\custom.css'},
}

# Prevent Pelican from processing the files in these directories (they are raw html)
ARTICLE_EXCLUDES = [
    'raw'
]

DISPLAY_TAGS_ON_SIDEBAR = False

TYPOGRIFY = True

PLUGIN_PATHS=['./plugins']

# the i18n and jinja stuff is from https://github.com/getpelican/pelican-themes/issues/482
PLUGINS = ['render_math','i18n_subsites']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

GOOGLE_ANALYTICS = "UA-155088985-1"
