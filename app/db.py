
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from crawler import AdDto
from typing import List
from sqlalchemy.exc import IntegrityError
import logging
import subprocess
import os
from datetime import datetime


Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(String, primary_key=True, index=True)
    url = Column(String)
    title = Column(String)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(String)
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String)
    datetime_found = Column(DateTime)

    def __init__(self, dto: AdDto):
        super().__init__()
        self.id = dto.hash
        self.url = dto.ad_url
        self.title = getattr(dto, 'title', None)
        self.price_usd = getattr(dto, 'price_usd', None)
        self.odometer = getattr(dto, 'odometer', None)
        self.username = getattr(dto, 'username', None)
        try:
            self.phone_number = str(getattr(dto, 'phone_number', None)[0])
        except (TypeError, IndexError):
            self.phone_number = None
        self.image_url = getattr(dto, 'image_url', None)
        self.images_count = getattr(dto, 'images_count', None)
        self.car_number = getattr(dto, 'car_number', None)
        self.car_vin = getattr(dto, 'car_vin', None)
        self.datetime_found = dto.datetime_found


class Database:

    def __init__(self, db_url):
        self.url = db_url
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(self.engine, autoflush=False, autocommit=False)
        Base.metadata.create_all(bind=self.engine)

    def add_ticket(self, dto: AdDto):
        ticket = Ticket(dto)
        try:
            with self.Session() as session:
                session.add(ticket)
                session.commit()
            logging.info(f'Succesfully saved: {dto.chart} {dto.title}')
        except IntegrityError:
            logging.warning(f'Duplicate ignored: {dto.title}')

    def get_all_tickets(self) -> List[Ticket]:
        with self.Session() as session:
            return session.query(Ticket).all()

    def dump(self):
        dump_path = f'../dumps/dump_{str(datetime.now())}.sql'
        os.makedirs(os.path.dirname(dump_path), exist_ok=True)

        cmd = ["pg_dump", self.url, "-f", dump_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        logging.debug(result)

        if result.returncode == 0:
            logging.info(f'Dump successful: {dump_path}')
            cmd = ["cat", dump_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            logging.debug(result.stdout)
        else:
            logging.info(f'Dump failed: {result.stderr}')
