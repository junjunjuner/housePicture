# -*- encoding: utf-8 -*-
'''
Created on $(DATE)

@author: jnnr

@requirments: Pycharm 2019.1; Python 3.5 | Anaconda 3(64-bit)

@decription:
'''
import requests
from bs4 import BeautifulSoup as bs
import re
import math
import pymongo
from urllib.parse import quote
from io import BytesIO
import bson.binary
import time
import random
import pandas as pd

# 存储酷家乐信息
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['kujiele_huxingtu']
coll = db['huxingtu_0906']

current_href = 'https://www.kujiale.com/huxing/beijing-%E7%BF%A1%E7%BF%A0%E8%A5%BF%E6%B9%96'
x = 1
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'authority': 'www.kujiale.com',
    'referer': current_href + '?__cdnfallback=true'
}
time.sleep(random.randint(2, 4))
req = requests.get(current_href, headers=headers, timeout=5)
soup = bs(req.text, 'lxml')
title = soup.find('div', class_='search-results').find('p', class_='title').get_text(strip=True)
number = re.findall('”的(.*?)个', title)[0]
pics = {}
build_info = {'楼盘名称': '翡翠西湖', '城市': '北京', '省份': '北京', '开盘时间': '2019年3月10日', '户型图数量': number,'链接':current_href}
print(build_info)
print(current_href)
pics['楼盘信息'] = build_info
if number == '200+':
    number = 200
    page = 14
else:
    number = int(number)
    page = math.ceil(int(number) / 15)
# 'tpl-huxingtu cell fl'
if page != 0:
    pic_hrefs = soup.find('ul', class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
    for p in pic_hrefs:
        try:
            kname = p.find('a', class_='name ell J_planLink').get_text(strip=True)
        except:
            kname = None
        try:
            jiegou = p.find('p', class_=re.compile('^detail g9')).find('span', class_='spec').get_text()
        except:
            jiegou = None
        try:
            area = p.find('p', class_=re.compile('^detail g9')).find('span', class_=None).get_text()
        except:
            area = None
        pic_href = p.find('img')['src']
        print(pic_href)
        # if 'http' in pic_href:
        #     time.sleep(1)
        #     pic_text = BytesIO(requests.get(pic_href).content)
        #     pic_bytes = bson.binary.Binary(pic_text.getvalue())
        # else:
        #     pic_bytes = None
        pic_name = ('户型图_%s') % str(x)
        x = x + 1
        pic_dict = {'户型图名称': pic_name, '酷家乐楼盘名': kname, '户型结构': jiegou, '建筑面积': area, '户型图链接': pic_href}
        # pic_dict = {'户型图名称': pic_name, '酷家乐楼盘名': kname, '户型结构': jiegou, '建筑面积': area, '户型图链接': pic_href,
        #             '户型图内容': pic_bytes}
        pics[pic_name] = pic_dict
    if page > 1:
        for i in range(2, page + 1):
            current_page = current_href + '/' + str(i)
            print(current_page)
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                'authority': 'www.kujiale.com',
                'referer': current_page + '?__cdnfallback=true'
            }
            time.sleep(random.randint(1, 3))
            req = requests.get(current_page, headers=headers, timeout=5)
            soup = bs(req.text, 'lxml')
            pic_hrefs = soup.find('ul', class_='cells j_cells clearfix').find_all('li',
                                                                                  class_=re.compile('^tpl-huxingtu'))
            for p in pic_hrefs:
                try:
                    kname = p.find('a', class_='name ell J_planLink').get_text(strip=True)
                except:
                    kname = None
                try:
                    jiegou = p.find('p', class_=re.compile('^detail g9')).find('span', class_='spec').get_text()
                except:
                    jiegou = None
                try:
                    area = p.find('p', class_=re.compile('^detail g9')).find('span', class_=None).get_text()
                except:
                    area = None
                pic_href = p.find('img')['src']
                print(pic_href)
                # if 'http' in pic_href:
                #     time.sleep(0.5)
                #     pic_text = BytesIO(requests.get(pic_href).content)
                #     pic_bytes = bson.binary.Binary(pic_text.getvalue())

                # else:
                    # pic_bytes = None
                pic_name = ('户型图_%s') % str(x)
                x = x + 1
                pic_dict = {'户型图名称': pic_name, '酷家乐楼盘名': kname, '户型结构': jiegou, '建筑面积': area, '户型图链接': pic_href}
                # pic_dict = {'户型图名称': pic_name, '酷家乐楼盘名': kname, '户型结构': jiegou, '建筑面积': area, '户型图链接': pic_href,
                #             '户型图内容': pic_bytes}
                pics[pic_name] = pic_dict
coll.insert(pics)
