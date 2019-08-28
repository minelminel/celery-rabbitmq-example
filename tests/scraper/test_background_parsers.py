import pytest

url = 'https://www.npr.org/sections/politics'

def test_background_parsers_base_is_abstract():
    from artifice.scraper.background.parsers.base import BaseParser
    with pytest.raises(TypeError):
        par = BaseParser(url)
    with pytest.raises(NotImplementedError):
        BaseParser._strain_links()
    with pytest.raises(NotImplementedError):
        BaseParser._extract_title()
    with pytest.raises(NotImplementedError):
        BaseParser._extract_text()
    with pytest.raises(NotImplementedError):
        BaseParser._extract_captions()
    with pytest.raises(NotImplementedError):
        BaseParser._extract_links()
    with pytest.raises(NotImplementedError):
        BaseParser.extract_content()

def test_background_parsers_base_has_methods():
    from artifice.scraper.background.parsers.base import BaseParser
    d = BaseParser.__dict__
    assert '_strain_links' in d
    assert '_extract_title' in d
    assert '_extract_text' in d
    assert '_extract_captions' in d
    assert '_extract_links' in d
    assert 'extract_content' in d

def test_background_parsers_npr():
    import requests
    from artifice.scraper.background.parsers import NPRParser
    par = NPRParser(requests.get(url))
    assert url in par.url
    assert par.soup is not None
    c = par.extract_content()
    assert isinstance(c.get('title'), str)
    assert isinstance(c.get('text'), str)
    assert isinstance(c.get('captions'), list)
    assert isinstance(c.get('url'), list)
    assert isinstance(c.get('origin'), str)
