from pathlib import Path

from worker import Worker


REPO_PATH = Path(__file__).resolve().parent.parent


if __name__ == '__main__':
    works = {
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
    public_dir = 'public'
    public_path = REPO_PATH/public_dir
    for name, kw_page in works.items():
        for keyword, page in kw_page:
            Worker(name, public_path, keyword, page)
            with open(public_path/'README.md', 'a') as f:
                path = f'{name}/{keyword}'
                f.write(f'''[{path}](./{public_dir}/{path}.md)''' + 2*'\n')
