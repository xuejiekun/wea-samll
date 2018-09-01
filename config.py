#!/usr/bin/python3
# -*- coding:utf-8 -*-
from pathlib import Path

class Config:
    # 测试header
    test_url = r'https://www.whatismybrowser.com/'

    # 数据源目录
    data_dir = r'res/data'

    # 数据源(测试)目录
    debug_data_dir = r'res/debug_data'

    #sqlite3数据库文件
    database_file = r'data.db'

    def __repr__(self):
        return '<Config\n' \
               '      data_dir : {}\n' \
               'debug_data_dir : {}\n' \
               ' database_file : {}>'.format(self.data_dir, self.debug_data_dir, self.database_file)


def makeconfig(lv=0):
    cf = Config
    for i in range(lv):
        cf.data_dir = Path('..', cf.data_dir)
        cf.debug_data_dir = Path('..', cf.debug_data_dir)
        cf.database_file = Path('..', cf.database_file)
    return cf


if __name__ == '__main__':
    config = makeconfig(2)
    a = config()
    print(type(config))
    print(a)
