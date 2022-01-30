from pathlib import Path

from worker import Worker


PUBLIC_DIR = Path(__file__).resolve().parent.parent/'public'


if __name__ == '__main__':
    boards = (
        'gossiping',
        'movie',
        'stupidclown',
        'stock',
    )
    for board in boards:
        Worker('ptt', PUBLIC_DIR, board, 200)

    keywords = (
        '後端',
        'python',
        '後端 python',
    )
    for keyword in keywords:
        Worker('104', PUBLIC_DIR, keyword, 200)
