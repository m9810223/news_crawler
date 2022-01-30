from crawlers.crawler import Crawler
from requests import request, Response


class PTTCrawler(Crawler):
    def __init__(self, board, page):
        super().__init__('https://www.ptt.cc', f'bbs/{board}/index.html', page)
        self.current_url = f'{self.host}/{self.init_path}'

    def crawl(self):
        response: Response = request('get', self.current_url, cookies={'over18': '1'})
        entries, next_path = self._parse(response.text)
        self.current_url = self.host+next_path
        return entries

    def _parse(self, data):
        soup = self._my_soup(data)
        entries = []
        elements = soup.select('#main-container > .r-list-container.action-bar-margin.bbs-screen > .r-ent')
        next_path = soup.select_one('.btn-group-paging a:nth-child(2)')['href']
        for element in elements:
            title = element.select_one('.title').select_one('a')
            if title is None:
                continue
            entries.append({
                'title': title.text,
                'link': self.host + title['href'],
                'push': element.select_one('.nrec').text,
            })
        return reversed(entries), next_path
