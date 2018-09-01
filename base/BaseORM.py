#!/usr/bin/python3
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseORM:

    def __init__(self, database, echo=False, autocommit=False):
        self.engine = create_engine(database, echo=echo)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession(autocommit=autocommit)

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
