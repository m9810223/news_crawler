from pathlib import Path
from sys import argv

from yaml import safe_load

from worker import Worker


DIR_PATH = Path(__file__).resolve().parent
REPO_PATH = DIR_PATH.parent


def yaml_load(path: Path):
    with open(path) as f:
        return safe_load(f.read())


if __name__ == '__main__':
    PRODUCTION = len(argv) > 1 and argv[1] in ('-p', '--production')
    works = yaml_load(DIR_PATH/'works.yaml')
    public_path = REPO_PATH/'public'
    Path.mkdir(public_path, parents=True, exist_ok=True)
    with open(public_path/'README.md', 'w') as f:
        f.write('![](https://github.com/m9810223/news_crawler/actions/workflows/update.yml/badge.svg)\n\n')
    for name, kw_page in works.items():
        for keyword, page in kw_page.items():
            if not PRODUCTION:
                page = 1
            Worker(name, public_path, keyword, page)
            with open(public_path/'README.md', 'a') as f:
                text = f'{name} - {keyword}'
                link = f'./{name}/{keyword}.md'.replace(' ', '%20')
                f.write(f'''[{text}]({link})''' + 2*'\n')
