import markdown
import re
import urllib
from os import chdir, listdir, path

'''
This function validates article names.

A valid article name consists of whitespace and word characters.
Returns True if a name is valid, otherwise False.
'''
def valid_article(article):
    if re.match('^[\w\s]+$', article):
        return True
    return False


'''
This function formats a menu according to internal rules.

Its arguments are a directory to search for articles and the current
article. Articles with invalid names are skipped.
'''
def format_menu(dir, article):
    items = []
    for file in sorted(listdir(dir)):
        if not valid_article(file):
            continue
        if file != article:
            template = '<a href="?¤article¤">¤article¤</a>'
        else:
            template = '<a id="current" href="?¤article¤">¤article¤</a>'
        items.append(template.replace('¤article¤',
                                      file))
    return '\n'.join(items)


'''
This function translates an article from markdown to HTML.

The function takes a directory to search for articles and
the name of the article to look for. 
Returns a 404 message for invalid an nonexistent articles.
'''
def format_article(dir, filename):
    notfound = '<p class="notfound">404</p>'
    if not valid_article(filename):
        return notfound
    file = path.join(dir, filename)
    if not path.isfile(file):
        return notfound
    with open(file) as f:
        html = markdown.markdown(f.read())
    return html


'''
This class constructs a page by using the provided template string.

The format method takes a title, an article and a menu, and inserts them 
into the template based on the tokens ¤title¤, ¤article¤ and ¤menu¤.

All arguments are expected to be fully formatted on submission.
'''
def format_page(template, title, article, menu):
    replacements = {'¤title¤': title,
                    '¤article¤': article,
                    '¤menu¤': menu}
    result = template
    for key in sorted(replacements.keys(), 
                      key=len,
                      reverse=True):
        result = result.replace(key, replacements[key])
    return result


'''
Central function to render an entire page given an article.

Takes the article to be rendered as an argument.
Returns the formatted page as a string.
'''
def render(article):
    articledir = 'articles'
    with open('page.html') as f:
        page = format_page(f.read(),
                           article,
                           format_article(articledir, article),
                           format_menu(articledir, article))
    return page


'''
WSGI entry point. Intended to be called by a WSGI-compliant web server.

Reads the article to be rendered from environ['QUERY_STRING'].
Writes the formatted result to the client.
'''
def application(environ, start_response):
    chdir(path.dirname(__file__))
    
    article = urllib.parse.unquote(environ['QUERY_STRING'])
    if not article:
        article = 'Hello world'

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
    article = 'Hello world'
    if len(sys.argv) > 1:
        article = sys.argv[1]
    print(render(article))
