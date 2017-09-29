from boilerpipe.extract import Extractor
from joblib import Memory
import numpy as np
import requests
import requests_cache

requests_cache.install_cache('page-cache', expire_after=60 * 60 * 24 * 10)

memory = Memory(cachedir="content-cache", verbose=1, bytes_limit=10**8)


def entry_content(entry):
    contents = [entry.description, entry.content[0].value,  entry.summary]
    return contents[np.argmin(map(len, contents))]

class FailedExtraction(Exception):
    pass


# see http://tomazkovacic.com/blog/2011/06/09/evaluating-text-extraction-algorithms/
def _scrape(url=None, html=None):
    assert (url != html)
    return Extractor(
        extractor='DefaultExtractor',
        html=html) if html is not None else _scrape(
            html=requests.get(url).content)


@_memory.cache(ignore=["entry"])
def url2html(url, entry=None):
    try:
        html = _scrape(url=url).getHTML()
        assert(html)
    except:
        html = '<h1>{title}</h1>\n'.format(title=entry.title) + entry_content(entry)
        assert(html)
    return html


@_memory.cache(ignore=["entry"])
def url2text(url, entry=None):
    try:
        text = _scrape(url=url).getText()
        if len(text) < 40:
            raise FailedExtraction
    except:
        text = (entry.title or '') + "." + (_scrape(html=entry_content(entry)).getText() or '')
        assert(text)
    return text


def entry2text(entry):
    return url2text(entry.link, entry)


def entry2html(entry):
    return url2html(entry.link, entry)