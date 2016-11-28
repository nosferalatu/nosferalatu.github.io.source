Title: Pelican and Math Equations
Date: 2016-11-27 12:00
Tags: Blog
Category: Blog
Slug: Pelican
Author: David Farrell
Summary: Pelican and Math Equations

This blog uses the static site generator [Pelican](http://www.getpelican.com). Here's how you can set up Pelican to
render LaTeX math equations.

In your Pelican content directory (mine is `c:\blog\source`), clone the [Pelican plugins
repository](https://github.com/getpelican/pelican-plugins):

    ::text
    cd c:\blog\source
    git submodule add https://github.com/getpelican/pelican-plugins.git plugins

Then modify your pelicanconf.py file to point at the path to the plugins and then which plugins you want to
use:

    :::text
    PLUGIN_PATHS=['./plugins']
    PLUGINS = ['render_math']

[render_math](https://github.com/getpelican/pelican-plugins/tree/master/render_math) is a Pelican plugin for rendering
LaTeX. That plugin extends Markdown so that anything in between `$...$` is rendered as math. For example:

`$x^2$` becomes $x^2$

`$e=mc^2$` becomes $e=mc^2$

`$\left| \nabla \phi \right| = 1$` becomes $\left| \nabla \phi \right| = 1$

You can also use `$$...$$` to put the equation in a new paragraph, like this: $$\dfrac {\partial \phi } {\partial t} + u \cdot \nabla \phi = 1$$

E-Z LaTeX
=========

I don't know LaTeX, but there are apps that will convert handwritten equations to LaTeX. I've been using an app called
MyScript that works well. They have a web demo here: [http://webdemo.myscript.com/views/math.html](http://webdemo.myscript.com/views/math.html)

With that, I can scribble some equations, and then cut and paste the LaTeX into Markdown, and easily create nice looking
equations.

