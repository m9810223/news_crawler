from pprint import pprint

from crawlers import PTTCrawler, Job104Crawler


if __name__ == '__main__':
    stock = PTTCrawler('stock', 2)
    pprint(stock())

    python = Job104Crawler('python', 2)
    pprint(python())
