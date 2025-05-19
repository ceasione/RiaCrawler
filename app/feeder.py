
from crawler import Crawler
import bs4
import asyncio


class Feeder:

    def __init__(self, networker, start_page, end_page, database, async_batch_size):

        self.networker = networker
        self.start_page = start_page
        self.end_page = end_page
        self.database = database
        self.async_batch_size = async_batch_size

    def _gather_page(self, page_n):
        html = self.networker.get_search_page(page_n).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tickets = soup.find_all('div', class_='content')
        urls = list()
        for ticket in tickets:
            try:
                urls.append(ticket.find('a', class_='address')['href'])
            except TypeError:
                continue
        return urls

    def process_batch(self, batch):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        crawlers = [Crawler(self.networker, ticket_link, database=self.database) for ticket_link in batch]

        loaders = [crawler.load() for crawler in crawlers]
        loop.run_until_complete(asyncio.gather(*loaders))

        processors = [crawler.process() for crawler in crawlers]
        loop.run_until_complete(asyncio.gather(*processors))

    def run(self):
        for page in range(self.start_page, self.end_page+1):

            urls_on_page = self._gather_page(page_n=page)
            while urls_on_page:
                batch = urls_on_page[:self.async_batch_size]
                del urls_on_page[:self.async_batch_size]
                self.process_batch(batch)
