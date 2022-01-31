from .crawler import Crawler


class Yourator(Crawler):
    def __init__(self, keyword, amount):
        super().__init__('https://www.yourator.co', f'jobs', amount)
        self.keyword = keyword
        self.current_count = 0

    def crawl(self):
        response = self.request(
            url=f'{self.host}/api/v2/jobs',
            params=(
                ('term[]', self.keyword),  # ('category[]', self.keyword),
                ('area[]', 'TPE'),
            ),
        )
        return self._parse(response.text)

    def _parse(self, data):
        obj = self._my_json_loads(data)
        jobs = obj.get('jobs')
        entries = []
        for job in jobs:
            title = job.get('name')
            link = self.host+job.get('path')
            entries.append({
                'title': title,
                'link': link,
                'company': job.get('company').get('brand'),
                'company_link': self.host+job.get('company').get('path'),
                'salary': job.get('salary'),
                **self._detail(link),
            })
            self.current_count += 1
            if self.current_count == self.amount:
                break
        return entries

    def _detail(self, url):
        response = self.request(url)
        soup = self._my_soup(response.text)
        elements = soup.select('.job-description > div > div > div > section')
        return {
            'description': elements[0].text.strip(),
            'other_condition': elements[1].text.strip(),
            'work_place': soup.select('.basic-info__address > a')[-1].text.strip(),
        }
