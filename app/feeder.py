
from crawler import Crawler
import bs4


class Feeder:

    def __init__(self, networker, start_page, end_page, database):

        self.networker = networker
        self.start_page = start_page
        self.end_page = end_page
        self.database = database

    def _gather_page(self, page_n):
        html = self.networker.get_search_page(page_n).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tickets = soup.find_all('div', class_='content')
        for ticket in tickets:
            try:
                yield ticket.find('a', class_='address')['href']
            except TypeError:
                continue

    def run(self):

        for page in range(self.start_page, self.end_page+1):
            for ticket_link in self._gather_page(page_n=page):
                crawler = Crawler(self.networker, ticket_link, database=self.database)
                crawler.process()
