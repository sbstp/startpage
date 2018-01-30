import json
from urllib.parse import quote
from bottle import get, run, jinja2_view as view, request, redirect


class Parser:

    def __init__(self):
        self._bangs = {}

    def add_bang(self, name, pattern):
        self._bangs[name] = pattern

    def get_url(self, query, default='g'):
        pattern = None
        parts = query.split(' ')
        for idx, part in enumerate(parts):
            if part.startswith("!") and len(part) > 1:
                bang = part[1:]
                try:
                    pattern = self._bangs[bang]
                    clean_query = ' '.join(parts[:idx] + parts[idx + 1:])
                    break
                except KeyError:
                    pass
        if pattern is None:
            pattern = self._bangs[default]
            clean_query = query
        clean_query = quote(clean_query)
        return pattern.format(clean_query)


p = Parser()
with open('config.json', 'r') as f:
    data = json.load(f)
    for key, val in data["bangs"].items():
        p.add_bang(key, val)


@get('/')
@view('index.html')
def index():
    return dict()


@get('/search')
def search():
    query = request.params['query']
    return redirect(p.get_url(query))


run(port=3000, reloader=True, debug=True)
