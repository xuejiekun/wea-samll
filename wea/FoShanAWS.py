#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import random
from pathlib import Path
from datetime import datetime, timedelta

from base import BaseRequests
from config import makeconfig


class FoShanAWS(BaseRequests):
    # 响应码
    FINISH = 0
    EXIST = 1
    EXPIRE= 2
    NOTFOUND = 4

    host = r'http://www.fs121.gov.cn'
    refer = r'http://www.fs121.gov.cn/wap/Awshour.aspx'

    def __init__(self, delay=2, timeout=5):
        super().__init__()
        self.delay = delay
        self.timeout = timeout

    # 生成数据地址
    # 格式 http://www.fs121.com/Awshour/dat/TQList-{ 时间 }.js?t={ 随机数 }
    @staticmethod
    def data_url(date):
        if date:
            return r'http://www.fs121.com/Awshour/dat/TQList-{}.js?t={}'.\
                format(date.strftime('%Y%m%d-%H00'),
                       random.random())

    # 设置目录和文件名
    def build_path(self, data_dir, date):
        # 设置下载目录(eg: data_dir/20180606/)
        down_dir = Path(data_dir, date.strftime('%Y%m%d'))
        os.makedirs(down_dir, exist_ok=True)

        # 设置文件名(eg: data_dir/20180606/20180606_1500.html)
        file = Path(data_dir, date.strftime('%Y%m%d'), '{}.html'.format(date.strftime('%Y%m%d_%H00')))
        return down_dir, file

    # 下载指定时间的数据
    def download_hour(self, data_dir, date, overwrite=False):
        down_dir, file = self.build_path(data_dir, date)

        # 数据文件已存在
        if file.exists() and not overwrite:
            print('[{}]数据文件已存在，不用下载.'.format(file.name))
            return self.EXIST

        # 请求数据
        while not self.get_page(self.data_url(date), timeout=self.timeout):
            print('请求超时，等待{}s重连'.format(self.timeout))
            time.sleep(self.timeout)

        # 过期
        if self.response.url == r'http://www.fs121.com/':
            print('请求的[{}]数据已过期.'.format(file.name))
            return self.EXPIRE

        # 找不到
        if self.response.status_code == 404:
            print('[{}] 找不到.'.format(file.name))
            return self.NOTFOUND

        # 保存
        self.save_as_html(file)
        print('下载完毕:{}'.format(self.response.url))
        return self.FINISH

    # 下载指定日期的数据
    def download_date(self, data_dir, date, overwrite=False):
        date = datetime(date.year, date.month, date.day)

        # 获取cookies
        self.get_page(self.refer)
        for i in range(24):
            code = self.download_hour(data_dir, date, overwrite=overwrite)
            date += timedelta(hours=1)
            if code != self.EXIST:
                time.sleep(self.delay * random.random())

    # 下载指定范围的数据
    def download_range(self, data_dir, start, end, overwrite=False):
        # 获取cookies
        self.get_page(self.refer)

        while start<= end:
            code = self.download_hour(data_dir, start, overwrite=overwrite)
            start += timedelta(hours=1)
            if code != self.EXIST:
                time.sleep(self.delay * random.random())

    # 下载今天的数据
    def download_today(self, data_dir, overwrite=False):
        end = datetime.now()
        start = datetime(end.year, end.month, end.day)
        self.download_range(data_dir, start, end, overwrite=overwrite)

    # 下载昨天的数据
    def download_yesterday(self, data_dir, overwrite=False):
        date = datetime.now()-timedelta(days=1)
        self.download_date(data_dir, date, overwrite=overwrite)


if __name__ == '__main__':
    cfg = makeconfig(1)

    catch = FoShanAWS()
    start = datetime(2018, 8, 30 , 0)
    end = datetime(2018, 8, 31 , 2)

    n = 5
    if n==1:
        # 测试1 下载指定小时
        catch.download_hour(cfg.debug_data_dir, start)

    elif n==2:
        # 测试2 下载指定日期
        catch.download_date(cfg.debug_data_dir, start)

    elif n==3:
        # 测试3 下载指定范围
        catch.download_range(cfg.debug_data_dir, start, end)

    elif n==4:
        # 测试4 下载今天
        catch.download_today(cfg.debug_data_dir)

    elif n==5:
        # 测试5 下载昨天
        catch.download_yesterday(cfg.debug_data_dir)
