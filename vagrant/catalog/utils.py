import re
from unicodedata import normalize
"""
    Utility functions and/or classes, some borrowed. Where borrowed, see the
    functions description for external reference.
"""
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
_PUNCT_RE = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """
        Generates an slightly worse ASCII-only slug.
        Borrowed from: http://flask.pocoo.org/snippets/5/

        Accepts:
            text: string containing value to be slugified
            delim: special delimiter to use for slugifying

        Returns:
            string value of the slugified text
    """
    result = []
    for word in _PUNCT_RE.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def request_wants_json(request):
    """
        Check to see if the client is asking for a JSON response or not.
        Borrowed from: http://flask.pocoo.org/snippets/45/

        Accepts:
            request: a flask.request object

        Returns: True if JSON should be returned to the client.
                 False if not.
    """
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def allowed_file(filename):
    ''' Check if filename provided matches allowed uploadable file types '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
