from typing import List, Set
from bs4 import BeautifulSoup
from collections import deque
from util import write_list_to_csv

import requests


class IKEASpider:
    def __init__(self, start_urls: List[str]):
        self.start_url = start_urls

    def crawl(self, visited=set()) -> Set[str]:
        def is_category(url):
            return "us/en/cat/" in url

        def is_product(url):
            return "us/en/p/" in url

        parsed = visited
        queue = deque(self.start_url)
        product_urls = set()
        cnt = 0
        print("Started...\n")
        while queue:
            cnt += 1
            curr_url = queue.popleft()
            if curr_url in parsed:
                continue

            parsed.add(curr_url)
            try:
                res = requests.get(curr_url)
                soup = BeautifulSoup(res.text, 'lxml')
                for anchor in soup.find_all(name='a'):
                    link = anchor.get('href')
                    if link is None or not is_category(link) and not is_product(link):
                        continue
                    if link not in queue and link not in parsed:
                        queue.append(link)
                    if is_product(link):
                        product_urls.add(link)
            except:
                print("Exception thrown when tried to request this url: ", curr_url)

            if cnt % 50 == 0:
                print("parsed urls:", len(parsed), ",  fetched product urls:", len(product_urls), ",  queue size:", len(queue))

        print("\ntotal urls parsed:", len(parsed), ",\ttotal product urls fetched:", len(product_urls))
        print("Finished.")

        return product_urls


if __name__ == '__main__':
    spider = IKEASpider(['https://www.ikea.com/us/en/cat/products-products/'])
    products = spider.crawl()
    write_list_to_csv(sorted(list(products)), './data/us_products_all.csv', 'product_url')
