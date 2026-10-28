#!/usr/bin/env python3
"""Verify the built static pages, or their production HTTP responses with --live."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://femalethreat.actor'
LIVE = '--live' in sys.argv

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.meta = {}
        self.links = []
        self.schemas = []
        self.schema = None
        self.h1s = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a.get('href'))
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content', '')
        if tag == 'a' and a.get('href', '').startswith('/'): self.links.append(a['href'])
        if tag == 'script' and a.get('type') == 'application/ld+json': self.schema = ''
        if tag == 'h1': self.h1s += 1
    def handle_data(self, text):
        if self.schema is not None: self.schema += text
    def handle_endtag(self, tag):
        if tag == 'script' and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None

def read(path):
    if LIVE:
        with urlopen(Request(ORIGIN + path, headers={'User-Agent': 'SkyPortfolioHealthCheck/1.0'}), timeout=30) as response:
            assert response.status == 200, (path, response.status)
            assert 'noindex' not in response.headers.get('X-Robots-Tag', '').lower(), path
            return response.read().decode()
    target = ROOT / 'dist' / path.lstrip('/')
    if target.is_dir(): target /= 'index.html'
    return target.read_text()

def verify():
    sitemap = ET.fromstring(read('/sitemap.xml'))
    urls = [n.text for n in sitemap.findall('{*}url/{*}loc')]
    assert len(urls) == len(set(urls)) and len(urls) >= 5, urls
    assert ORIGIN + '/' in urls and ORIGIN + '/about' in urls
    assert f'Sitemap: {ORIGIN}/sitemap.xml' in read('/robots.txt')
    results = []
    for url in urls:
        assert url.startswith(ORIGIN + '/'), url
        path = urlparse(url).path
        html = read(path)
        page = Page()
        page.feed(html)
        assert page.canonical == [url], (path, page.canonical)
        assert page.meta.get('author') == 'Sky Blu DeGrate', path
        assert page.meta.get('og:url') == url, path
        assert page.meta.get('description'), path
        assert 'noindex' not in page.meta.get('robots', '').lower(), path
        assert page.h1s == 1, (path, page.h1s)
        assert len(page.schemas) == 1, path
        graph = page.schemas[0]['@graph']
        types = {n['@type'] for n in graph}
        assert 'Person' in types and 'WebSite' in types, path
        assert any(n.get('name') == 'Sky Blu DeGrate' for n in graph), path
        if path == '/about': assert 'ProfilePage' in types, path
        if path.startswith('/case-files/'):
            assert 'BlogPosting' in types and 'rel="author"' in html, path
            assert 'What this case demonstrates' in html, path
        for link in page.links:
            link_path = urlparse(link).path
            target = ROOT / 'dist' / link_path.lstrip('/')
            assert target.exists() or (target / 'index.html').exists(), (path, link)
        results.append({'url': url, 'canonical': page.canonical[0], 'schema_types': sorted(types), 'status': 'passed'})
    return {'mode': 'live' if LIVE else 'build', 'pages': results, 'sitemap': 'passed', 'robots': 'passed'}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
