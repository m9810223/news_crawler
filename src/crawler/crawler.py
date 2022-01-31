from pathlib import Path
from abc import ABC, abstractmethod
from functools import partial
from json import loads

from requests import request
from bs4 import BeautifulSoup

REPO_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = Path(__file__).resolve().parent.parent/'public'


class Crawler(ABC):
    _my_soup = partial(BeautifulSoup, features="html.parser")
    _my_json_loads = partial(loads)

    def __init__(self, host, init_path, page):
        self.host = host
        self.init_path = init_path
        self.page = page

    def __call__(self):
        result = []
        for _ in range(self.page):
            entries = self.crawl()
            result.extend(entries)
        return result

    def request(self, url, method='get', **kwargs):
        return request(method, url, **kwargs)

    @abstractmethod
    def crawl(self):
        return NotImplemented
