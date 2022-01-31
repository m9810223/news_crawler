from pathlib import Path

from crawler import PTT, Job104, Yourator
from writer import PTTWriter, Job104Writer, YouratorWriter


works = {
    'ptt': (PTT, PTTWriter),
    '104': (Job104, Job104Writer),
    'yourator': (Yourator, YouratorWriter),
}


class Worker:
    def __init__(self, work_name, folder: Path, keyword,  page):
        self.work_name = work_name.lower()
        self.keyword = keyword.lower()
        crawler, writer = works[self.work_name]
        self.crawler = crawler(keyword, page)
        self.writer = writer(folder/self.work_name/keyword)
        self.start()

    def start(self):
        print(f'{self.work_name} - {self.keyword}')
        self.writer.write(self.crawler())
