from .crawler import Crawler


class Job104(Crawler):
    def __init__(self, keyword, amount):
        super().__init__('https://www.104.com.tw', f'104/{keyword}', amount)
        self.keyword = keyword
        self.current_page = 1
        self.visited = set()

    def crawl(self):
        response = self.request(
            url=f'{self.host}/jobs/search/',
            params=(
                ('keyword', self.keyword),
                ('isnew', '14'),
                ('area', '6001001000'),
                ('page', f'{self.current_page}'),
            ),
        )
        self.current_page += 1
        return self._parse(response.text)

    def _parse(self, data):
        soup = self._my_soup(data)
        entries = []
        elements = soup.select(
            'article.b-block--top-bord.job-list-item.b-clearfix.js-job-item'
            ':not(.js-job-item--focus.b-block--ad)'
        )
        for element in elements:
            title = element.select_one('.b-block__left > .b-tit > a')
            if title is None:
                continue
            link = f'https:{title["href"]}'
            company = element.select_one('.b-block__left > .b-list-inline.b-clearfix > li:nth-child(2) > a')
            if link in self.visited:
                continue
            self.visited.add(link)
            entries.append({
                'title': title.text,
                'link': link,
                'company': company.text.strip(),
                'company_link': f'https:{company["href"]}',
                **self._details(link),
            })
        return entries

    def _remove_redundants(self, text: str):
        redundants = (
            ('\n'*3, '\n'*2),
        )
        for old, new in redundants:
            while old in text:
                text = text.replace(old, new)
        return text

    def _details(self, url):
        content_id = url.split('/')[-1].split('?')[0]
        response = self.request(
            url=f'{self.host}/job/ajax/content/{content_id}',
            headers={'Referer': url},
        )
        obj = self._my_json_loads(response.text)
        return {
            'description': self._remove_redundants(obj['data']['jobDetail']['jobDescription']),
            'salary': obj['data']['jobDetail']['salary'],
            'other_condition': self._remove_redundants(obj['data']['condition']['other']),
            'work_place': f"{obj['data']['jobDetail']['addressRegion']}({obj['data']['jobDetail']['industryArea']})",
        }
