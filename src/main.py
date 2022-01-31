from pathlib import Path
from sys import argv

from worker import Worker


REPO_PATH = Path(__file__).resolve().parent.parent


if __name__ == '__main__':
    PRODUCTION = len(argv) > 1 and argv[1] in ('-p', '--production')
    works = {
        'yourator': (
            ('後端工程', 10),
        ),
        'ptt': (
            ('gossiping', 200),
            ('movie', 200),
            ('stupidclown', 200),
            ('stock', 200),
        ),
        '104': (
            ('後端 python', 10),
        ),
    }
    public_path = REPO_PATH/'public'
    Path.mkdir(public_path, parents=True, exist_ok=True)
    with open(public_path/'README.md', 'w') as f:
        f.write('![](https://github.com/m9810223/news_crawler/actions/workflows/update.yml/badge.svg?branch=public)\n\n')
        f.write('![](https://github.com/m9810223/news_crawler/actions/workflows/update.yml/badge.svg)\n\n')
    for name, kw_page in works.items():
        for keyword, page in kw_page:
            if not PRODUCTION:
                page = 1
            Worker(name, public_path, keyword, page)
            with open(public_path/'README.md', 'a') as f:
                text = f'{name} - {keyword}'
                link = f'./{name}/{keyword}.md'.replace(' ', '%20')
                f.write(f'''[{text}]({link})''' + 2*'\n')
