
import bs4
import re
import json
from datetime import datetime
import logging
from typing import List


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
    hash = None

    def finalize(self):
        _d = self.__dict__.copy()
        _d.pop('phone_number')

        self.hash = str(hex(hash(tuple(sorted(_d.items())))))
        self.datetime_found = datetime.now()


class Crawler:
    def __init__(self, networker, ticket, database):
        self.URL = ticket
        self.networker = networker
        self.html = self.networker.get_ticket_page(self.URL).text
        self.soup = bs4.BeautifulSoup(self.html, 'html.parser')
        self.database = database

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

    def _phone_number_extract(self, dto):
        """
        Makes additional request to RIA API extracting secured numbers
        :return:
        """
        _hash = self.soup.find('script', class_=re.compile(r"(js-user-secure-)\w+")).get('data-hash')
        _id = re.search(r'_\d+.html', self.URL).group()[1:-5]

        try:
            raw = self.networker.get_phone(_id, _hash).text
            response = json.loads(raw)
        except json.JSONDecodeError as e:
            logging.error(f'Cannot parse response from secure phone API\n\n{raw}')
            raise e
        phones = [item['phoneFormatted'] for item in response['phones']]

        dto.phone_number = []
        for phone in phones:
            _f = '+38' + ''.join([char for char in phone if char in '0123456789'])
            dto.phone_number.append(AdDto.PhoneNumber(_f))

    def _image_url_extract(self, dto):
        dto.image_url = self.soup.find('div', class_='carousel-inner').find('picture').find('source')['srcset']

    def _images_count_extract(self, dto):
        _str = self.soup.find('span', class_='count').find(class_='mhide').text.strip()
        _int = int(''.join([char for char in _str if char in '0123456789']))
        dto.images_count = _int

    def _car_number_extract(self, dto):
        try:
            dto.car_number = self.soup.find('span', class_='state-num').text.strip()[:10]
        except AttributeError:
            pass

    def _car_vin_extract(self, dto):
        try:
            dto.car_vin = self.soup.find('span', class_='vin-code').text.strip()
        except AttributeError:
            pass
        try:
            dto.car_vin = self.soup.find('span', class_='label-vin').text.strip()
        except AttributeError:
            pass

    # noinspection PyArgumentList
    def process(self):
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
            self._car_vin_extract
        ]
        for stage in pipeline:
            try:
                stage(dto)
            except (AttributeError, TypeError, IndexError):
                logging.warning(f'Stage {stage} failed on {dto.ad_url}')
                continue
        dto.finalize()
        self.database.add_ticket(dto)
        return dto
