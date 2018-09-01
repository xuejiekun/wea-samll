#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


class BaseRequests:
    DEFAULT_USERAGENT = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    DEFAULT_ACCEPT_LANGUAGE = r'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.DEFAULT_USERAGENT,
                                     'Accept-Language': self.DEFAULT_ACCEPT_LANGUAGE})

    # 设置请求头
    def set_headers(self, useragent):
        self.session.headers.update({'User-Agent': useragent})

    # 设置referer
    def set_referer(self, referer):
        self.session.headers.update({'Referer': referer})

    # 清空referer
    def clear_referer(self):
        self.session.headers.pop('Referer')

    # get请求
    def get_page(self, url, timeout=10, **kwargs):
        try:
            self.response = self.session.get(url, timeout=timeout, **kwargs)
        except:
            return False
        return True

    # post请求
    def post_page(self, url, data=None, json=None, timeout=10, **kwargs):
        try:
            self.response = self.session.post(url, data=data, json=json, timeout=timeout, **kwargs)
        except:
            return False
        return True

    # 获取特定编码的text
    def text(self, encoding=None):
        if encoding:
            encoding_save = self.response.encoding
            self.response.encoding = encoding
            text = self.response.text
            self.response.encoding = encoding_save
            return text
        return self.response.text

    # 返回json
    def json(self, **kwargs):
        return self.response.json(**kwargs)

    # 获取网页标题
    def get_title(self):
        self.bsobj = BeautifulSoup(self.response.content, 'lxml')
        return self.bsobj.title.text

    # 将请求内容保存为图片
    def save_as_pic(self, filename='1.jpg'):
        with open(filename, 'wb') as fp:
            fp.write(self.response.content)

    # 将当前页面保存为html
    def save_as_html(self, filename='1.html'):
        with open(filename, 'wb', ) as fp:
            fp.write(self.response.content)


if __name__ == '__main__':
    br = BaseRequests()
    br.get_page(r'https://www.baidu.com')
    br.save_as_html('{}.html'.format(br.get_title()))
