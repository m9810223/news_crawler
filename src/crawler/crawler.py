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

    def __init__(self, host, init_path, amount):
        self.host = host
        self.init_path = init_path
        self.amount = amount

    def __call__(self):
        result = []
        i = 0
        while i < self.amount:
            entries = self.crawl()
            result.extend(entries)
            i += len(entries)
        return result[:self.amount]

    def request(self, url, method='get', **kwargs):
        return request(method, url, **kwargs)

    @abstractmethod
    def crawl(self):
        return NotImplemented
