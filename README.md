# blog.py

A minimalist blogging application.

## What?

The idea is to be able to write markdown-formatted text files, commit to git, push and forget.

The application reads its contents from the hard-coded subdirectory  ```articles/``` and uses a few hard-coded templates contained under ```support/```. Creation and modification times of articles are read from the git log for a given article.

## Setup

You will need a python environment that fulfills ```requirements.txt```. A venv is recommended.

## Running the application

```blog.py``` can be called directly on the command line, expecting the first argument to be the article to be rendered. It will output the rendered HTML for that article.

The application can also be run as a WSGI application under a web server. This has been tested on apache2.4 with mod_wsgi on Debian.

When running under WSGI, the application reads the article to be rendered from ```environ['QUERY_STRING']```.
