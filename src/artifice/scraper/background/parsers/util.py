def remove_duplicates(lst):
    return list(dict.fromkeys(lst))

def url_root(url):
    from urllib.parse import urlparse
    return 'https://{}'.format(urlparse(url).netloc)
