from .base import BaseParser
from .util import remove_duplicates, url_root


class NPRParser(BaseParser):
    def __init__(self, response):
        from bs4 import BeautifulSoup
        self.url = response.url
        self.soup = BeautifulSoup(response.content, 'html.parser')

    @staticmethod
    def _strain_links(url, links):
        root = url_root(url)
        keep = []
        for link in links:
            if not link:
                pass
            elif (link[0] == "#") or (len(link) < 2):
                pass
            elif root not in link:
                pass
            else:
                keep.append(link.strip())
        return keep

    def _extract_title(self):
        if self.soup.title:
            try:
                return str(self.soup.title.text)
            except:
                return ''

    def _extract_text(self):
        p_tags = [e.get_text() for e in self.soup.find_all('p', {})]
        article = '\n'.join(p_tags)
        washed = " ".join(article.split())
        return str(washed)

    def _extract_captions(self):
        captions = []
        for p in self.soup.find_all('p'):
            try:
                if 'caption' in p['class']:
                    captions.append(p.text)
            except:
                pass
        return captions

    def _extract_links(self):
        all_links = remove_duplicates([str(link.get('href')) for link in self.soup.find_all('a')])
        return self._strain_links(self.url, all_links)

    def extract_content(self):
        title = self._extract_title()
        text = self._extract_text()
        captions = self._extract_captions()
        url = self._extract_links()
        origin = self.url
        return dict(title=title, text=text, captions=captions, url=url, origin=origin)
