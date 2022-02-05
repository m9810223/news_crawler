from .crawler import Crawler


class Yourator(Crawler):
    def __init__(self, keyword, amount):
        super().__init__('https://www.yourator.co', f'jobs', amount)
        self.keyword = keyword
        self.current_count = 0
        self.visited = set()
        self.current_page = 1

    def crawl(self):
        response = self.request(
            url=f'{self.host}/api/v2/jobs',
            params=(
                ('term[]', self.keyword),
                ('area[]', 'TPE'),
                ('page', self.current_page),
            ),
        )
        self.current_page += 1
        return self._parse(response.text)

    def _parse(self, data):
        obj = self._my_json_loads(data)
        jobs = obj.get('jobs')
        entries = []
        for job in jobs:
            title = job.get('name')
            link = self.host+job.get('path')
            if link in self.visited:
                continue
            self.visited.add(link)
            entries.append({
                'title': title,
                'link': link,
                'company': job.get('company').get('brand'),
                'company_link': self.host+job.get('company').get('path'),
                'salary': job.get('salary'),
                **self._details(link),
            })
            self.current_count += 1
            if self.current_count == self.amount:
                break
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
        response = self.request(url)
        soup = self._my_soup(response.text)
        elements = soup.select('.job-description > div > div > div > section')
        return {
            'description': self._remove_redundants(elements[0].text.strip()),
            'other_condition': self._remove_redundants(elements[1].text.strip()),
            'work_place': soup.select('.basic-info__address > a')[-1].text.strip(),
        }
