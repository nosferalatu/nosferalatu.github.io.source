Title: Setting Up This Blog
Date: 2014-5-26 13:00
Tags: Blog
Category: Blog
Slug: setting-up
Author: David Farrell
Summary: Setting Up This Blog
This blog uses the static site generator [Pelican](http://www.getpelican.com) and is hosted on [Github](http://www.github.com). Here are a few notes on how I set things up.

Installing Pelican
------------------

First, get Python 2.7, and get the Python package manager Pip. For Windows, you can follow the instructions [here](http://docs.python-guide.org/en/latest/starting/install/win/).

Make a directory for your blog, such as `c:\blog`. Then, `pip install pelican` and if you want Markdown support `pip install markdown`. Many online guides suggest you put Pelican into a Python virtualenv. That's not necessary, but it keeps things tidy, so I made a virtualenv at `c:\blog` and installed Pelican using Pip like this:

    :::text
    virtualenv virtualenv-pelican
    cd virtualenv-pelican\scripts
    activate
    pip install pelican markdown

Creating The Blog
-------------------

Next, I set up the blog for Pelican. I put the source content that Pelican processes into `c:\blog\source` and the generated HTML into `c:\blog\site` by doing this:

    :::text
    md c:\blog\source c:\blog\site
    cd c:\blog\source
    pelican-quickstart

The default answers to the questions are usually reasonable, but season to taste.

By default, Pelican puts the generated HTML into the `output` directory relative to pelicanconf.py. I prefer to call it the `site` directory and have it sit side-by-side the `source` directory because it makes the Github setup a bit cleaner. I edited the `pelicanconf.py` and changed the `OUTPUTPATH` variable to point to `c:\blog\site`:

    :::text
    OUTPUT_PATH = '../site'

Then add a post in the `content` directory at `c:\blog\source\content`. A simple Markdown post should work:

    :::text
    Title: First Post
    Date: 2014-5-26 12:00
    Tags: Blog
    Category: Blog
    Slug: first-post
    Author: David Farrell
    Summary: First Post
    It's so easy when everybody's trying to please me, baby

We should be able to generate the blog now. Try this:

    :::text
    make html
    make serve

Browse to `127.0.0.1:8000` and, hey, it works!

Live Editing
------------

In one shell, run `make regenerate`. This automatically regenerates the `site` directory whenever you change a file in the `source` directory. In another shell, run the local web server `make serve`. Now you can change any file, refresh your browser, and immediately see your changes.

The command `make devserver` will also do that, but it calls a Bash script, which doesn't work on Windows.

Pelican Themes
--------------

The default Pelican theme isn't spectacular. You can get additional themes by cloning the Pelican theme repository:

    :::text
    cd c:\blog\source
    git clone https://github.com/getpelican/pelican-themes themes

You'll find all the themes in the new `themes` directory. To choose one, set the `THEME` variable in `pelicanconf.py`:

    :::text
    THEME = 'themes/pelican-bootstrap3'

I like the Pelican-Bootstrap3 theme. It has a `README.md` that you'll want to read. The Bootstrap theme is actually themed itself with [Bootswatch](http://bootswatch.com/). You can also easily customize the CSS and set the syntax highlighting style. Here's the relevant bits in my `pelicanconf.py`:

    :::text
    BOOTSTRAP_THEME = 'cyborg'        # Bootswatch sub-theme for Bootstrap
    PYGMENTS_STYLE = 'monokai'        # Syntax highlighting theme
    CUSTOM_CSS = 'static\custom.css'
    STATIC_PATHS=['images','extra\custom.css']
    EXTRA_PATH_METADATA = {'extra\custom.css': {'path': 'static\custom.css'}}

The full `extra\custom.css` path is `c:\blog\source\content\extra\custom.css` (some of Pelican's paths were relative to the `content` directory). The only thing my custom.css does right now is change the backtick block highlighting colors; for some reason, those colors don't change with the Bootstrap theme or subthemes. Here's what that looks like:

    :::text
    code {
     padding:2px 4px;
     font-size:90%;
     white-space:nowrap;
     background-color:#080808;
     color:#b0b0b0;
     border-radius:4px
    }

Google Analytics
----------------

Google Analytics can be set up by following the instructions here: [Google Analytics With Pelican](https://matthewdevaney.com/posts/2019/03/17/google-analytics-with-pelican/)

Once you have modified the publishconf.py with your analytics tracking number, you need to run the command `make publish` instead of `make html` to have the tracking code included. You want to `make publish` once you are ready to generate the pages that will go live, and `make html` when you are generating pages to view your changes locally.

Github Pages Hosting
--------------------

I'm using [Github Pages](https://pages.github.com/) to host this blog. I created two repositories. One is named `nosferalatu.github.io` and holds the blog site, and the other is named `nosferalatu.github.io.source` and holds the Pelican source for the blog. You can configure git branches to hold everything in a single repo, but I thought it was more straightforward to just use two repositories.

I cleaned up the `themes` directory to remove the themes I don't want (otherwise, that directory is around 176 megs). I then init both repositories and push them to Github with this:

    :::text
    cd c:\blog\site
    git init
    git add -A .
    git commit -m "initial commit"
    git remote add origin https://github.com/nosferalatu/nosferalatu.github.io.git
    git push -u origin master
    cd c:\blog\source
    git init
    git add -A .
    git commit -m "initial commit"
    git remote add origin https://github.com/nosferalatu/nosferalatu.github.io.source.git
    git push -u origin master

A few minutes later, the blog appears at [nosferalatu.github.io](http://nosferalatu.github.io). 
