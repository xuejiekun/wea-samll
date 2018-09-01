#!/usr/bin/python3
# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from base import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(80), unique=True, nullable=False)
    eng_name = Column(String(120))
    lng = Column(Float)
    lat = Column(Float)
    road = Column(String(10))
    code = Column(String(10))

    dats = relationship('Dat', backref='address', lazy='dynamic')


class Dat(Base):
    __tablename__ = 'dat'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    temp = Column(Float)
    rainfall = Column(Float)
    wdir = Column(Integer)
    speed = Column(Float)
    logtime = Column(DateTime, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        UniqueConstraint('logtime', 'address_id'),
    )
