# models.py
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RoadAddressCode(Base):
    __tablename__ = 'road_address_code'

    address_code = Column(String(12), primary_key=True)
    address_name = Column(String(80))
    address_name_en = Column(String(80))
    eupmyeondong_serial = Column(String(2), primary_key=True)
    sido_name = Column(String(20))
    sido_name_en = Column(String(40))
    sigungu_name = Column(String(20))
    sigungu_name_en = Column(String(40))
    eupmyeondong_name = Column(String(20))
    eupmyeondong_name_en = Column(String(40))
    is_eupmyeondong = Column(String(1))
    eupmyeondong_code = Column(String(3))
    is_used = Column(String(1))
    modification_reason = Column(String(1))
    modification_history = Column(String(14))
    registerdate = Column(String(8))
    expireddate = Column(String(8))
