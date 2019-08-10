from urllib.parse import urlparse
from bs4 import BeautifulSoup as BS


def pour_soup(response):
    return BS(response.content, 'html.parser')


class NPRParser(object):
    def __init__(self, url, response):
        self.url = url
        self.soup = pour_soup(response)

    @staticmethod
    def _strain_links(root, links):
        keep = []
        for link in links:
            if not link:
                pass
            elif (link[0] is "#") or (len(link) < 2):
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
                pass

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
        all_links = list(set([str(link.get('href')) for link in self.soup.find_all('a')]))
        url_root = f'http://{urlparse(self.url).netloc}'
        return self._strain_links(url_root, all_links)

    def extract_content(self):
        title = self._extract_title()
        text = self._extract_text()
        captions = self._extract_captions()
        links = self._extract_links()
        return dict(title=title,text=text,captions=captions,links=links,url=self.url)
