from pathlib import Path
import logging
from sys import stdout

from crawler import PTT, Job104
from writer import PTTWriter, Job104Writer


works = {
    'ptt': (PTT, PTTWriter),
    '104': (Job104, Job104Writer),
}


class Worker:
    def __init__(self, work_name, folder: Path, keyword,  page):
        self.work_name = work_name.lower()
        self.keyword = keyword.lower()
        crawler, writer = works[self.work_name]
        self.crawler = crawler(keyword, page)
        self.writer = writer(folder/self.work_name/keyword)
        self.setup_logger()
        self.start()

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler(stdout))

    def start(self):
        self.logger.debug(f'{self.work_name} -> {self.keyword}')
        self.writer.write(self.crawler())
