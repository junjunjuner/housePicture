# -*- encoding: utf-8 -*-
'''
Created on $(DATE)

@author: jnnr

@requirments: Pycharm 2019.1; Python 3.5 | Anaconda 3(64-bit)

@decription:酷家乐户型图
'''
import requests
from bs4 import BeautifulSoup as bs
import re
import math
import pymongo
from urllib.parse import quote
from io import BytesIO
import bson.binary
import pandas as pd
# 存储酷家乐信息
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['kuojiele_huxingtu']
coll = db['huxingtu']
# 读取酷家乐网站
client1 = pymongo.MongoClient('127.0.0.1',port=27017)
kuojialehref_coll = client1['HousePlan']['kujiale_href']
# 读取房天下数据
client2 = pymongo.MongoClient('172.28.171.58',port=27017)
fang_coll = client2['fang']['loupan']
for fang in fang_coll.find():
    # print(fang)
    fang_city = fang['city']
    if fang_city == '枣阳':
        fang_city = '襄阳'
    fang_loupan = fang['lou_name']
    if '/' in fang_loupan:
        fang_loupan = re.split('/',fang_loupan)[0]
    fang_time = fang['lou_time']
    kcity_info = kuojialehref_coll.find_one({'city':fang_city})
    if kcity_info != None:
        kcity_city = kcity_info['city']
        kcity_href = kcity_info['href']
        kcity_province = kcity_info['province']
    else:
        kcity_city = None
        kcity_href = None
        kcity_province = None
    print(kcity_city,kcity_province,kcity_href)
    # client = pymongo.MongoClient('127.0.0.1',27017)
    # # 存储酷家乐信息
    # db = client['kuojiele_huxingtu']
    # coll = db['huxingtu']
    current_href = kcity_href + '-' + quote(fang_loupan)
    # 15条
    # current_href = 'https://www.kujiale.com/huxing/foshan-%E5%85%AC%E5%9B%AD%E8%A5%BF%E4%BE%A7A%E5%9C%B0%E5%9D%97%E5%AE%89%E7%BD%AE%E5%B0%8F%E5%8C%BA'
    # 0条
    # current_href = 'https://www.kujiale.com/huxing/foshan-ceshi'

    x = 1
    # 35条
    # current_href = 'https://www.kujiale.com/huxing/foshan-%E8%BF%9E%E5%B9%B3%E8%8A%B1%E5%9B%AD'
    print(current_href)

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'authority': 'www.kujiale.com',
        'referer': current_href + '?__cdnfallback=true'
    }
    req = requests.get(current_href, headers=headers, timeout=5)
    soup = bs(req.text, 'lxml')
    title = soup.find('div', class_='search-results').find('p', class_='title').get_text(strip=True)
    number = re.findall('”的(.*?)个',title)[0]
    pics = {}
    build_info = {'楼盘名称': '连平花园', '城市': '佛山', '省份': '广东', '开盘时间': '2019年底', '户型图数量': number}
    pics['楼盘信息'] = build_info
    print(number)
    if number == '200+':
        number = 200
        page = 14
    else:
        number = int(number)
        page = math.ceil(int(number)/15)
    # 'tpl-huxingtu cell fl'
    if page != 0:
        pic_hrefs = soup.find('ul',class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
        print(len(pic_hrefs))
        for p in pic_hrefs:
            try:
                jiegou = p.find('p', class_=re.compile('^detail g9')).find('span', class_='spec').get_text()
            except:
                jiegou = None
            try:
                area = p.find('p', class_=re.compile('^detail g9')).find('span', class_=None).get_text()
            except:
                area = None
            pic_href = p.find('img')['src']
            if 'http' in pic_href:
                pic_text = BytesIO(requests.get(pic_href).content)
                pic_bytes = bson.binary.Binary(pic_text.getvalue())
            else:
                pic_bytes = None
            pic_name = ('户型图%s')%str(x)
            x = x + 1
            pic_dict = {'户型图':pic_name,'户型结构':jiegou,'建筑面积':area,'户型图链接':pic_href,'户型图内容':pic_bytes}
            pics[pic_name] = pic_dict
        if page > 1:
            for i in range(2,page+1):
                print(i)
                current_page = 'https://www.kujiale.com/huxing/beijing-%E6%96%B0%E5%85%89%E5%A4%A7%E4%B8%AD%E5%BF%83/'+str(i)
                print(current_page)
                headers = {
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                    'authority': 'www.kujiale.com',
                    'referer': current_page + '?__cdnfallback=true'
                }
                req = requests.get(current_page, headers=headers, timeout=5)
                soup = bs(req.text, 'lxml')
                pic_hrefs = soup.find('ul',class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
                print(len(pic_hrefs))
                for p in pic_hrefs:
                    try:
                        jiegou = p.find('p', class_=re.compile('^detail g9')).find('span',class_='spec').get_text()
                    except:
                        jiegou = None
                    try:
                        area = p.find('p', class_=re.compile('^detail g9')).find('span',class_=None).get_text()
                    except:
                        area = None
                    pic_href = p.find('img')['src']
                    if 'http' in pic_href:
                        pic_text = BytesIO(requests.get(pic_href).content)
                        pic_bytes = bson.binary.Binary(pic_text.getvalue())

                    else:
                        pic_bytes = None
                    pic_name = ('户型图%s') % str(x)
                    x = x + 1
                    pic_dict = {'户型图': pic_name, '户型结构': jiegou, '建筑面积': area, '户型图链接': pic_href,
                                '户型图内容': pic_bytes}
                    pics[pic_name] = pic_dict
    coll.insert(pics)

