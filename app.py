#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
from datetime import datetime, timedelta

from wea.FoShanAWS import FoShanAWS
from wea.DataManager import DataManager
from config import makeconfig


def get_mysql_address():
    user = os.getenv('mysqlu')
    passwd = os.getenv('mysqlp')
    if user and passwd:
        return 'mysql+mysqlconnector://{}:{}@localhost:3306/wea'.format(user, passwd)
    return None


if __name__ == '__main__':
    cfg = makeconfig()
    catch = FoShanAWS()
    catch.download_yesterday(cfg.debug_data_dir)

    mysql_address = get_mysql_address()
    if mysql_address:
        with DataManager(mysql_address) as db:
            down_dir, file = catch.build_path(cfg.debug_data_dir, datetime.now()-timedelta(days=1))
            print('正在更新[{}]的数据...'.format(down_dir))
            db.insert_dir(down_dir)
            print('更新完毕!')
