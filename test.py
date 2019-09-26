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
from io import BytesIO
import bson.binary
current_href = 'https://www.kujiale.com/huxing/beijing-%E7%BF%A1%E7%BF%A0%E8%A5%BF%E6%B9%96'
print(current_href)
#
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
build_info = {'楼盘名称': '翡翠西湖', '城市': '北京', '省份': '北京', '开盘时间': '2019年3月10日', '户型图数量': number}
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
    # print(soup)
    pic_hrefs = soup.find('ul', class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
    for p in pic_hrefs:
        # print(p)
        try:
            kname = p.find('a',class_='name ell J_planLink').get_text(strip=True)
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
        print(kname,jiegou,area,pic_href)
    pic_hrefs = soup.find('ul',class_='cells j_cells clearfix').find_all('li', class_=re.compile('^tpl-huxingtu'))
    print(len(pic_hrefs))
    for p in pic_hrefs:
        pic_span = p.find('p',class_=re.compile('^detail g9')).find_all('span')
        pic_info = [span.get_text() for span in pic_span]
        pic_href = p.find('img')['src']
        if 'http' in pic_href:
            pic_text = BytesIO(requests.get(pic_href).content)
            pic_bytes = bson.binary.Binary(pic_text.getvalue())
        else:
            pic_bytes = None
