from urllib.parse import urlparse


def get_second_level_domain(url: str):
    netloc = urlparse(url).netloc.split('.')
    return netloc[-2] if len(netloc) > 1 else ""
