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
import time
import random
import pandas as pd
# 存储酷家乐信息
skip_num = 0
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['kujiale_huxingtu']
coll = db['huxingtu_info']
# 读取酷家乐网站
client1 = pymongo.MongoClient('127.0.0.1',port=27017)
kuojialehref_coll = client1['HousePlan']['kujiale_href']
# 读取房天下数据
client2 = pymongo.MongoClient('172.28.171.58',port=27017)
fang_coll = client2['fang']['loupan']
for fang in fang_coll.find(no_cursor_timeout=True).skip(27277):
    # print(fang)
    skip_num = skip_num + 1
    print(skip_num)
    if skip_num%1000 == 0:
        time.sleep(random.randint(600,1200))
    fang_city = fang['city']
    if fang_city == '枣阳':
        fang_city = '襄阳'
    fang_loupan = fang['lou_name']
    if '/' in fang_loupan:
        fang_loupan = re.split('/',fang_loupan)[0]
    fang_time = fang['lou_time']
    kcity_info = kuojialehref_coll.find_one({'city':fang_city},no_cursor_timeout = True)
    if kcity_info != None:
        kcity_city = kcity_info['city']
        kcity_href = kcity_info['href']
        kcity_province = kcity_info['province']
    else:
        kcity_city = None
        kcity_href = None
        kcity_province = None
        continue

    current_href = kcity_href + '-' + quote(fang_loupan)
    print(current_href)
    x = 1
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'authority': 'www.kujiale.com',
        'referer': current_href + '?__cdnfallback=true'
    }
    time.sleep(random.randint(2,4))
    try:
        req = requests.get(current_href, headers=headers, timeout=5)
    except:
        time.sleep(random.randint(600,1200))
        req = requests.get(current_href, headers=headers)

    soup = bs(req.text, 'lxml')
    try:
        title = soup.find('div', class_='search-results').find('p', class_='title').get_text(strip=True)
        number = re.findall('”的(.*?)个', title)[0]
    except:
        number = 0
    pics = {}
    build_info = {'楼盘名称': fang_loupan, '城市': kcity_city, '省份': kcity_province, '开盘时间': fang_time, '户型图数量': number,'链接':current_href}
    print(build_info)
    pics['楼盘信息'] = build_info
    if coll.find_one({'楼盘信息.链接': current_href}):
        print("吼哈，该信息已保存：",build_info)
        continue
    if number == '200+':
        number = 200
        page = 14
    else:
        number = int(number)
        page = math.ceil(int(number)/15)
    # 'tpl-huxingtu cell fl'
    if page != 0:
        try:
            pic_hrefs = soup.find('ul',class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
        except:
            with open('fail.txt','a') as f:
                f.write('信息有误 '+str(current_href)+'\n')
            pic_hrefs = []
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
            pic_href = p.find('img')['src'].split('@')[0]
            # if 'http' in pic_href:
            #     time.sleep(1)
            #     pic_text = BytesIO(requests.get(pic_href).content)
            #     pic_bytes = bson.binary.Binary(pic_text.getvalue())
            # else:
            #     pic_bytes = None
            pic_name = ('户型图_%s')%str(x)
            x = x + 1
            pic_dict = {'户型图名称':pic_name,'酷家乐楼盘名':kname,'户型结构':jiegou,'建筑面积':area,'户型图链接':pic_href}
            pics[pic_name] = pic_dict
        if page > 1:
            for i in range(2,page+1):
                current_page = current_href + '/' + str(i)
                print(current_page)
                headers = {
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                    'authority': 'www.kujiale.com',
                    'referer': current_page + '?__cdnfallback=true'
                }
                time.sleep(random.randint(1,3))
                try:
                    req = requests.get(current_page, headers=headers, timeout=5)
                except:
                    time.sleep(random.randint(600, 1200))
                    req = requests.get(current_page, headers=headers)
                soup = bs(req.text, 'lxml')
                pic_hrefs = soup.find('ul',class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
                for p in pic_hrefs:
                    try:
                        kname = p.find('a', class_='name ell J_planLink').get_text(strip=True)
                    except:
                        kname = None
                    try:
                        jiegou = p.find('p', class_=re.compile('^detail g9')).find('span',class_='spec').get_text()
                    except:
                        jiegou = None
                    try:
                        area = p.find('p', class_=re.compile('^detail g9')).find('span',class_=None).get_text()
                    except:
                        area = None
                    pic_href = p.find('img')['src'].split('@')[0]
                    # if 'http' in pic_href:
                    #     time.sleep(0.5)
                    #     pic_text = BytesIO(requests.get(pic_href).content)
                    #     pic_bytes = bson.binary.Binary(pic_text.getvalue())
                    #
                    # else:
                    #     pic_bytes = None
                    pic_name = ('户型图_%s') % str(x)
                    x = x + 1
                    pic_dict = {'户型图名称': pic_name, '酷家乐楼盘名': kname, '户型结构': jiegou, '建筑面积': area, '户型图链接': pic_href}
                    pics[pic_name] = pic_dict
    if not coll.find_one({'楼盘信息.链接': current_href}):
        coll.insert(pics)
    else:
        print('该信息已保存:',build_info)
