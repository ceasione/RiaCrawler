
import bs4
import re
import json
from datetime import datetime
import logging
from typing import List
import inspect


class AdDto:

    class PhoneNumber:
        prefix: str
        number: str

        def __init__(self, raw):
            self.prefix = raw[:4]
            self.number = raw[4:]

        def get_num(self):
            return self.prefix + self.number

        def __str__(self):
            return self.get_num()

    ad_url: str
    title: str
    price_usd: int
    odometer: int
    username: str
    phone_number: List[PhoneNumber]
    image_url: str
    images_count: int
    car_number: str
    car_vin: str
    datetime_found: datetime
    chart = None
    hash = None

    def _make_chart(self):
        chart = '['
        chart += '*' if getattr(self, 'ad_url', None) is not None else '-'
        chart += '*' if getattr(self, 'title', None) is not None else '-'
        chart += '*' if getattr(self, 'price_usd', None) is not None else '-'
        chart += '*' if getattr(self, 'odometer', None) is not None else '-'
        chart += '*' if getattr(self, 'username', None) is not None else '-'
        chart += '*' if getattr(self, 'phone_number', None) is not None else '-'
        chart += '*' if getattr(self, 'image_url', None) is not None else '-'
        chart += '*' if getattr(self, 'images_count', None) is not None else '-'
        chart += '*' if getattr(self, 'car_number', None) is not None else '-'
        chart += '*' if getattr(self, 'car_vin', None) is not None else '-'
        return chart + ']'

    def finalize(self):
        _d = self.__dict__.copy()
        _d.pop('phone_number', None)

        self.hash = str(hex(hash(tuple(sorted(_d.items())))))
        self.chart = self._make_chart()
        self.datetime_found = datetime.now()


class Crawler:
    def __init__(self, networker, ticket, database):
        self.URL = ticket
        self.networker = networker
        self.database = database
        self.html = None
        self.soup = None
        self.loaded = False

    def _url_extract(self, dto):
        dto.ad_url = self.URL

    def _title_extract(self, dto):
        dto.title = self.soup.find('h1', class_='head').text.strip()

    def _price_usd_extract(self, dto):
        _str = self.soup.find('div', class_='price_value').find('strong').text.strip()
        dto.price_usd = int(''.join(char for char in _str if char in '0123456789'))

    def _odometer_extract(self, dto):
        dto.odometer = int(self.soup.find('div', class_='base-information').find('span').text.strip()) * 1000

    def _username_extract(self, dto):
        dto.username = self.soup.find(class_='seller_info_name').text.strip()

    @staticmethod
    def __get_title(raw: str):
        start_tag = '<title>'
        end_tag = '</title>'
        s = raw.find(start_tag)
        e = raw.find(end_tag)
        if -1 < s < e and e > -1:
            return raw[s + len(start_tag):e].strip()
        else:
            return 'Undefined error'


    async def _phone_number_extract(self, dto):
        """
        Makes additional request to RIA API extracting secured numbers
        :return:
        """
        _hash = self.soup.find('script', class_=re.compile(r"(js-user-secure-)\w+")).get('data-hash')
        _id = re.search(r'_\d+.html', self.URL).group()[1:-5]

        raw = await self.networker.get_phone_async(_id, _hash)
        try:
            response = json.loads(raw)
        except json.JSONDecodeError as e:
            logging.error(f'Cannot parse response from secure phone API: {self.__get_title(raw)} _id: {_id} _hash: {_hash}')
            raise e
        phones = [item['phoneFormatted'] for item in response['phones']]

        dto.phone_number = []
        for phone in phones:
            _f = '+38' + ''.join([char for char in phone if char in '0123456789'])
            dto.phone_number.append(AdDto.PhoneNumber(_f))
        logging.debug(f'Success parse response from secure phone API: {self.__get_title(raw)} _id: {_id} _hash: {_hash}')

    def _image_url_extract(self, dto):
        dto.image_url = self.soup.find('div', class_='carousel-inner').find('picture').find('source')['srcset']

    def _images_count_extract(self, dto):
        _str = self.soup.find('span', class_='count').find(class_='mhide').text.strip()
        _int = int(''.join([char for char in _str if char in '0123456789']))
        dto.images_count = _int

    def _car_number_extract(self, dto):
        dto.car_number = self.soup.find('span', class_='state-num').text.strip()[:10]

    def _car_vin_attempt1_extract(self, dto):
        dto.car_vin = self.soup.find('span', class_='vin-code').text.strip()

    def _car_vin_attempt2_extract(self, dto):
        dto.car_vin = self.soup.find('span', class_='label-vin').text.strip()

    async def load(self):
        self.html = await self.networker.get_ticket_page_async(self.URL)
        self.soup = bs4.BeautifulSoup(self.html, 'html.parser')
        self.loaded = True

    # noinspection PyArgumentList
    async def process(self):
        dto = AdDto()
        pipeline = [
            self._url_extract,
            self._title_extract,
            self._price_usd_extract,
            self._odometer_extract,
            self._username_extract,
            self._phone_number_extract,
            self._image_url_extract,
            self._images_count_extract,
            self._car_number_extract,
            self._car_vin_attempt1_extract,
            self._car_vin_attempt2_extract
        ]
        for stage in pipeline:
            try:
                ret = stage(dto)
                if inspect.iscoroutine(ret):
                    await ret
            except (AttributeError, TypeError, IndexError, json.JSONDecodeError, KeyError):
                logging.debug(f'Stage {stage} failed on {dto.ad_url}')
                continue
        dto.finalize()
        self.database.add_ticket(dto)  # TODO make async
        return dto
