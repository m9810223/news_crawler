from .crawler import Crawler
from requests import request, Response


class Job104(Crawler):
    def __init__(self, keyword, page):
        super().__init__('https://www.104.com.tw', f'104/{keyword}', page)
        self.keyword = keyword
        self.current_page = 1

    def crawl(self):
        response: Response = request(
            'get',
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
            entries.append({
                'title': title.text,
                'link': link,
                'company': company.text.strip(),
                'company_link': f'https:{company["href"]}',
                **self._job_detail(link),
            })
        return entries

    def _job_detail(self, url):
        content_id = url.split('/')[-1].split('?')[0]
        response = request(
            'get',
            url=f'https://www.104.com.tw/job/ajax/content/{content_id}',
            headers={'Referer': url},
        )
        obj = self._my_json_loads(response.text)
        return {
            'description': obj['data']['jobDetail']['jobDescription'],
            'salary': obj['data']['jobDetail']['salary'],
            'other_condition': obj['data']['condition']['other'],
            'work_place': f"{obj['data']['jobDetail']['addressRegion']}({obj['data']['jobDetail']['industryArea']})",
        }
