from pathlib import Path

from crawler import PTT, Job104
from writer import PTTWriter, Job104Writer


works = {
    'ptt': (PTT, PTTWriter),
    '104': (Job104, Job104Writer),
}


class Worker:
    def __init__(self, work_name, folder: Path, keyword,  page):
        work_name = work_name.lower()
        crawler, writer = works[work_name]
        self.crawler = crawler(keyword, page)
        self.writer = writer(folder/work_name/keyword)
        # start
        self.writer.write(self.crawler())
