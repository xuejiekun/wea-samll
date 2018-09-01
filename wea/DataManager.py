#!/usr/bin/python3
# -*- coding:utf-8 -*-
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import and_
from base import BaseORM
from wea.Models import Address, Dat


class FileData:
    NAME = 0
    TEMP = 1
    RAINFALL = 2
    WDIR = 3
    SPEED = 4

    LNG =5
    LAT = 6
    ROAD = 7
    ENG_NAME = 8
    CODE = 9

    def __init__(self, file):
        self.datas = []
        self.file = Path(file)
        self.name = self.file.name
        self.get_dat()

    # 读取数据文件，返回list
    def get_dat(self):
        if not self.file.exists():
            print('文件[{}]不存在.'.format(self.file.name))
            return

        print('读取数据文件:{}'.format(self.file.name))
        with self.file.open('rb') as fp:
            try:
                self.datas = json.loads(fp.read(), encoding='utf-8')
            except:
                print('数据文件格式不正确.')
                return


class DataManager(BaseORM):

    def __init__(self, database, echo=False, autocommit=False):
        super().__init__(database, echo, autocommit)

    def insert_address(self, name, eng_name, lng, lat, road, code):
        addr = self.session.query(Address).filter(Address.name == name).first()
        if not addr:
            addr = Address(name=name, eng_name=eng_name, lng=lng, lat=lat, road=road, code=code)
            self.session.add(addr)
            self.commit()
        return addr

    def insert_dat(self, temp, rainfall, wdir, speed, logtime, addr):
        dat = self.session.query(Dat).filter(and_(Dat.logtime == logtime, Dat.address_id == addr.id)).first()
        if not dat:
            dat = Dat(temp=temp, rainfall=rainfall, wdir=wdir, speed=speed, logtime=logtime, address_id=addr.id)
            self.session.add(dat)
            self.commit()
            print(r'插入[{} {}]数据成功.'.format(logtime, addr.name))
        return dat

    def insert_file(self, file):
        fd = FileData(file)
        logtime = datetime.strptime(fd.name.split('.')[0], '%Y%m%d_%H00')
        for data in fd.datas:
            data = list(map(lambda x: None if not x else x, data))
            addr = self.insert_address(name=data[FileData.NAME],
                                       eng_name=data[FileData.ENG_NAME],
                                       lng=data[FileData.LNG],
                                       lat=data[FileData.LAT],
                                       road=data[FileData.ROAD],
                                       code=data[FileData.CODE])

            dat = self.insert_dat(temp=data[FileData.TEMP],
                                  rainfall=data[FileData.RAINFALL],
                                  wdir=data[FileData.WDIR],
                                  speed=data[FileData.SPEED],
                                  logtime=logtime,
                                  addr=addr)
            # print(data)

    def insert_dir(self, dir):
        dir = Path(dir)
        for file in dir.rglob('*.html'):
            self.insert_file(file)


if __name__ == '__main__':
    db = DataManager('sqlite:///data.db')
    db.create_table()
    db.insert_dir(r'F:\Project\Python\web_catch\wea-small\res\debug_data')
    db.close()