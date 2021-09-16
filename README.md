# blog.py

A minimalist blogging application.

[gitHub](https://github.com/booski/blog)

## What?

The aim of the application is to enable a minimalist blogging site, whose entire publishing workflow is based around a git repo. Every page generated by this application follows the same general pattern: A list of available articles along with the text of the requested article.

In order to keep track of important metadata such as creation and modification times, git is used as a database of sorts. The application reads articles from the subdirectory ```articles/```, which is expected to be a git repository. The commit history of a given article provides all necessary metadata.

The idea is to make all publishing happen via git, removing the need for an administrative interface while allowing a very streamlined publishing process. When writing a new article, all that is required to publish is simply to commit and push the file.

The HTML output of the program is entirely defined by the files under ```support/```, except of course the article contents which are produced from markdown.

## Setup

You will need a python3.7+ environment that fulfills ```requirements.txt```. A venv is recommended. The application doesn't need write access to anything. Read access is necessary for the ```articles/``` and ```support/``` subdirectories.

If you don't push directly to the web server's copy of the repo under ```articles/```, you will need some way to keep the articles up to date. One way would be a scheduled task periodically pulling the repo. You could probably also set up a github web hook to trigger a pull whenever you push something. 🤷


## Running the application

For ease of debugging, ```blog.py``` can be called directly on the command line. It expects the first argument to be the name of the article to be rendered (so it will need to be quoted if it contains spaces). It will output the rendered HTML for that article.

The application is generally intended to be run as a WSGI application under a web server. The testing stack is apache2.4 with mod_wsgi on Debian.

When running under WSGI, the application reads the article to be rendered from ```environ['PATH_INFO']```. Make sure any static files (mainly ```style.css```, but probably anything under ```public```) is exposed by the web server so the client can fetch them. ```blog.py``` will not serve any such files on its own.
