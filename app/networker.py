
import requests
import aiohttp


class Networker:

    def __init__(self,
                 user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                 ui='cf5b99af255b707f',
                 sessid_long='eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjM0Nzg4ODY4MzEsIndlYkNsaWVudENvZGUiOjYyNjc0OTU2Nywid2ViQ2xpZW50Q29va2llIjoiY2Y1Yjk5YWYyNTViNzA3ZiIsIl9leHBpcmUiOjE3NDY4MDc2NjcwMDUsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==',
                 sessid_short='9PNl1E33Q7-pQgjJLDEUgpXO0pJSAFsn'):

        self.cookies = {
            'Path': '/',
            'chk': '1',
            '__utmc': '79960839',
            '__utmz': '79960839.1746721241.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'showNewFeatures': '7',
            'extendedSearch': '1',
            'informerIndex': '1',
            '_gcl_au': '1.1.1140414341.1746721241',
            '_ga': 'GA1.1.209738481.1746721241',
            '_504c2': 'http://10.42.15.139:3000',
            '_fbp': 'fb.1.1746721241779.43450619175270889',
            'gdpr': '[]',
            'ui': ui,
            'PHPSESSID': sessid_long,
            'test_new_features': '841',
            'advanced_search_test': '42',
            'ipp': '100',
            'showNewNextAdvertisement': '10',
            'PHPSESSID': sessid_short,
            'ab-link-video-stories': '2',
            'news_prior': '%7B%22item0%22%3A5%2C%22item1%22%3A4%2C%22item2%22%3A3%2C%22item3%22%3A2%7D',
            'test_fast_search': '3',
            '__utma': '79960839.2146687449.1746721241.1746721241.1746724782.2',
            '__utmt': '1',
            '__utmt_b': '1',
            '__gads': 'ID=bc713e1b9e843536:T=1746721429:RT=1746724784:S=ALNI_MYbb1HJM1j_Av1HTpNVvyxY57Lj1Q',
            '__gpi': 'UID=000010a6c4eb0cbe:T=1746721429:RT=1746724784:S=ALNI_MYxuSWFz7MECHOKUyp_xlozMf18uw',
            '__eoi': 'ID=db2470fc07fc9ebb:T=1746721429:RT=1746724784:S=AA-AfjbYBgMGYL7E5zJfcbTx28-q',
            '__utmb': '79960839.4.10.1746724782',
            '_ga_KGL740D7XD': 'GS2.1.s1746724626$o2$g1$t1746724817$j13$l0$h1635055105',
            'promolink2': '3',
            'FCNEC': '%5B%5B%22AKsRol_Qvm2xETuhC46j6wU5rlracOY9ssl92GurZ8na7MyNz2lYa8kCnINcKpMGbTXHn5kY636Jm_u3tq2GFP7O03WxM3z_uIMuxidLqytaEEPovdP29MhmI4JbEi3r57n92XKlGkasgXUJY3wcjacTXp_ofjp0vA%3D%3D%22%5D%5D',
        }

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,uk;q=0.8,ru;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://auto.ria.com/uk/',
            'sec-ch-ua': '"Chromium";v="135", "Not-A.Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            # 'cookie': 'Path=/; Path=/; chk=1; __utmc=79960839; __utmz=79960839.1746721241.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); showNewFeatures=7; extendedSearch=1; informerIndex=1; _gcl_au=1.1.1140414341.1746721241; _ga=GA1.1.209738481.1746721241; _504c2=http://10.42.15.139:3000; _fbp=fb.1.1746721241779.43450619175270889; gdpr=[]; ui=cf5b99af255b707f; PHPSESSID=eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjM0Nzg4ODY4MzEsIndlYkNsaWVudENvZGUiOjYyNjc0OTU2Nywid2ViQ2xpZW50Q29va2llIjoiY2Y1Yjk5YWYyNTViNzA3ZiIsIl9leHBpcmUiOjE3NDY4MDc2NjcwMDUsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==; test_new_features=841; advanced_search_test=42; ipp=100; showNewNextAdvertisement=10; PHPSESSID=9PNl1E33Q7-pQgjJLDEUgpXO0pJSAFsn; ab-link-video-stories=2; news_prior=%7B%22item0%22%3A5%2C%22item1%22%3A4%2C%22item2%22%3A3%2C%22item3%22%3A2%7D; test_fast_search=3; __utma=79960839.2146687449.1746721241.1746721241.1746724782.2; __utmt=1; __utmt_b=1; __gads=ID=bc713e1b9e843536:T=1746721429:RT=1746724784:S=ALNI_MYbb1HJM1j_Av1HTpNVvyxY57Lj1Q; __gpi=UID=000010a6c4eb0cbe:T=1746721429:RT=1746724784:S=ALNI_MYxuSWFz7MECHOKUyp_xlozMf18uw; __eoi=ID=db2470fc07fc9ebb:T=1746721429:RT=1746724784:S=AA-AfjbYBgMGYL7E5zJfcbTx28-q; __utmb=79960839.4.10.1746724782; _ga_KGL740D7XD=GS2.1.s1746724626$o2$g1$t1746724817$j13$l0$h1635055105; promolink2=3; FCNEC=%5B%5B%22AKsRol_Qvm2xETuhC46j6wU5rlracOY9ssl92GurZ8na7MyNz2lYa8kCnINcKpMGbTXHn5kY636Jm_u3tq2GFP7O03WxM3z_uIMuxidLqytaEEPovdP29MhmI4JbEi3r57n92XKlGkasgXUJY3wcjacTXp_ofjp0vA%3D%3D%22%5D%5D',
        }

    def get_search_page(self, page_n):
        params = {
            'lang_id': '4',
            'page': str(page_n),
            'countpage': '100',
            'indexName': 'auto',
            'custom': '1',
            'abroad': '2',
        }

        return requests.get('https://auto.ria.com/uk/search/',
                            params=params, cookies=self.cookies, headers=self.headers)

    def get_ticket_page(self, url):

        return requests.get(url, cookies=self.cookies, headers=self.headers)

    def get_phone(self, _id, _hash):
        params = {
            'hash': _hash,
            'expires': '2592000',
        }
        return requests.get(f'https://auto.ria.com/users/phones/{_id}',
                            params=params, cookies=self.cookies, headers=self.headers)

    async def get_ticket_page_async(self, url):
        async with aiohttp.ClientSession(cookies=self.cookies, headers=self.headers) as session:
            async with session.get(url) as response:
                return await response.text()

    async def get_phone_async(self, _id, _hash):
        params = {
            'hash': _hash,
            'expires': '2592000',
        }
        async with aiohttp.ClientSession(cookies=self.cookies, headers=self.headers) as session:
            async with session.get(f'https://auto.ria.com/users/phones/{_id}', params=params) as response:
                return await response.text()
