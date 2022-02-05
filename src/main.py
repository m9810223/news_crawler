from pathlib import Path
from sys import argv

from yaml import safe_load as yaml_load

from worker import Worker


DIR_PATH = Path(__file__).resolve().parent
REPO_PATH = DIR_PATH.parent


def load_yaml(path: Path):
    with open(path) as f:
        return yaml_load(f.read())


if __name__ == '__main__':
    PRODUCTION = len(argv) > 1 and argv[1] in ('-p', '--production')
    works = load_yaml(DIR_PATH/'works.yaml')
    publish_path = REPO_PATH/'docs'
    Path.mkdir(publish_path, parents=True, exist_ok=True)
    with open(publish_path/'README.md', 'w') as f:
        f.write('![](https://github.com/m9810223/news_crawler/actions/workflows/update.yml/badge.svg)'+'\n'*2)
    with open(publish_path/'_config.yml', 'w') as f:
        f.write('theme: jekyll-theme-cayman' + '\n')
    for name, kw_page in works.items():
        for keyword, page in kw_page.items():
            if not PRODUCTION:
                page = 1
            Worker(name, publish_path, keyword, page)
            with open(publish_path/'README.md', 'a') as f:
                text = f'{name} - {keyword}'
                link = f'https://m9810223.github.io/news_crawler/{name}/{keyword}'.replace(' ', '%20')
                f.write(f'[{text}]({link})'+'\n'*2)
