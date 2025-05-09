
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from crawler import AdDto
from typing import List
from sqlalchemy.exc import IntegrityError
import logging


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
        self.title = dto.title if dto.title else None
        self.price_usd = dto.price_usd if dto.price_usd else None
        self.odometer = dto.odometer if dto.odometer else None
        self.username = getattr(dto, 'username', None)  # dto.username if dto.username else None
        self.phone_number = str(dto.phone_number[0]) if dto.phone_number else None
        self.image_url = dto.image_url if dto.image_url else None
        self.images_count = dto.images_count if dto.images_count else None
        self.car_number = getattr(dto, 'car_number', None)  # dto.car_number if dto.car_number else None
        self.car_vin = dto.car_vin if dto.car_vin else None
        self.datetime_found = dto.datetime_found


class Database:

    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(self.engine, autoflush=False, autocommit=False)
        Base.metadata.create_all(bind=self.engine)

    def add_ticket(self, dto: AdDto):
        ticket = Ticket(dto)
        try:
            with self.Session() as session:
                session.add(ticket)
                session.commit()
            logging.info(f'Succesfully saved: {dto.title}')
        except IntegrityError:
            logging.warning(f'Duplicate ignored: {dto.title}')

    def get_all_tickets(self) -> List[Ticket]:
        with self.Session() as session:
            return session.query(Ticket).all()

    def dump(self):
        # TODO implement
        pass
