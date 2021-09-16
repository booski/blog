import re
import urllib
from os import chdir, listdir, path

import markdown
from git import Repo

'''
This function validates article names.

Returns True if a name is valid, otherwise False.
'''
def valid_article(article):
    if article.startswith('.'):
       return False
    if article.endswith('.draft'):
       return False
    if not re.match('^[\w\s\.,;!?%-]+$', article):
       return False
    return True


'''
This function formats a menu according to internal rules.

Its arguments are a directory to search for articles and the current
article. Articles with invalid names are skipped.

Returns the formatted menu.
'''
def format_menu(articledir, article):
    items = []
    for item in sorted(listdir(articledir)):
        if not valid_article(item):
            continue
        if item != article:
            template = '<a href="/¤quoted¤">¤article¤</a>'
        else:
            template = '<a id="current" href="/¤quoted¤">¤article¤</a>'
        items.append(render_template(template,
                                     article=item,
                                     quoted=urllib.parse.quote(item)))
    return '\n'.join(items)


'''
This function renders a template by replacing its tokens with provided values.

It accepts a template followed by the desired replacements as key-value mapped 
pairs. Each key is wrapped in leading and trailing '¤' characters and used to 
search the template for placeholders to be replaced by the corresponding value.
'''
def render_template(template, **replacements):
    result = template
    for key in sorted(replacements.keys(), 
                      key=len,
                      reverse=True):
        result = result.replace('¤'+key+'¤', replacements[key])
    return result
    

'''
This function translates an article from markdown to HTML.

It accepts a template, the article text in markdown format, the creation date,
and an optional updated date, and returns the rendered result.

The arguments date and modified are expected to be Datetime objects or None.
If date is None, no date info is rendered. If modified is None, no modification
info is rendered.
'''
def format_article(template, text, date, modified=None):
    ctime_vis = 'hidden'
    ctime = ''
    if date:
        ctime_vis = 'visible'
        ctime = date.strftime('%Y/%m/%d %H:%M')
    mtime_vis = 'hidden'
    mtime = ''
    if modified:
        mtime_vis = 'visible'
        mtime = modified.strftime('%Y/%m/%d %H:%M')
    return render_template(template,
                           text=markdown.markdown(text),
                           ctime_visibility=ctime_vis,
                           ctime=ctime,
                           mtime_visibility=mtime_vis,
                           mtime=mtime)


'''
This function formats a page given a page template and some content blocks.

It takes a template, a title, an article and a menu, and returns the 
rendered result.

All arguments are expected to be fully formatted as strings on submission.
'''
def format_page(template, title, article, menu):
    return render_template(template,
                           title=title,
                           article=article,
                           menu=menu)


'''
Central function to render an entire page given an article.

Takes the article to be rendered as an argument.
Returns the formatted page as a string.

The directory containing all articles is hard-coded here.
'''
def render(article):
    articledir = 'articles'
    try:
        assert valid_article(article)
        articlefile = path.join(articledir, article)
        assert path.isfile(articlefile)
        repo = Repo(articledir)
        # An ugly, ugly hack:
        commits = repo.iter_commits(paths=article)
        mtime = ctime = next(commits)
        for ctime in commits:
            pass
        # hack over.
        if ctime != mtime:
            mtime = mtime.committed_datetime
        else:
            mtime = None
        ctime = ctime.committed_datetime
    except AssertionError as e:
        article="4oh4oh4..."
        articlefile = 'support/404.html'
        ctime = ''
        mtime = ''
    except StopIteration as e:
        ctime = None
        mtime = None
    with open('support/page.html') as ptempl, \
         open('support/article.html') as atempl, \
         open(articlefile) as atext:
        page = format_page(ptempl.read(),
                           article,
                           format_article(atempl.read(),
                                          atext.read(),
                                          ctime,
                                          mtime),
                           format_menu(articledir, article))
    return page


'''
WSGI entry point. Intended to be called by a WSGI-compliant web server.

Reads the article to be rendered from environ['PATH_INFO'].
Writes the formatted result to the client.
'''
def application(environ, start_response):
    chdir(path.dirname(__file__))
    
    article = urllib.parse.unquote(environ['PATH_INFO'])[1:]
    if not article:
        article = 'README.md'

    status = '200 OK'
    if not valid_article(article):
        status = '404 Not Found'

    output = render(article)
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [bytes(output, 'utf-8')]

'''
Standalone entry point.

Argv[1] should contain the name of the article to be rendered.
Prints the formatted result to stdout.
'''
if __name__ == '__main__':
    import sys
    article = 'README.md'
    if len(sys.argv) > 1:
        article = sys.argv[1]
    print(render(article))
