# -*- encoding: utf-8 -*-
'''
Created on $(DATE)

@author: jnnr

@requirments: Pycharm 2019.1; Python 3.5 | Anaconda 3(64-bit)

@decription:  mongodb 保存图片信息（gridfs、bson）
'''
# url = 'https://qhtbdoss.kujiale.com/fpimgnew/prod/3FO458YKNI7V/l/LSH2JIAKN4FBGAABAAAAABQ8.jpg'
#
# x = url.split('@')[0]
# print(x)

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

# # bson方式
#
# # 存储酷家乐信息
# client = pymongo.MongoClient('127.0.0.1', 27017)
# db = client['kujiele_huxingtu']
# coll = db['huxingtu_0906']
# for datas in coll.find(no_cursor_timeout=True):
#     id = datas['_id']
#     print(id)
#     for (key,value) in datas.items():
#         if key.startswith('户型图'):
#             pic_href = value['户型图链接'].split('@')[0]
#             print(pic_href)
#             if 'http' in pic_href:
#                 time.sleep(0.5)
#                 pic_text = BytesIO(requests.get(pic_href).content)
#                 pic_bytes = bson.binary.Binary(pic_text.getvalue())
#
#             else:
#                 pic_bytes = None
#             value['户型图内容'] = pic_bytes
#             coll.update_one({'_id':id},{'$set':{key:value}})
#         # coll.update_one()

# 导出
# import pymongo
# import re
# client = pymongo.MongoClient('localhost',27017)
# cursor = client['kujiele_huxingtu']['huxingtu_0905']
#
# # data = cursor.find_one({'楼盘信息.楼盘名称': {'$regex': '京贸国际城'}})
# data = cursor.find_one({'楼盘信息.楼盘名称': '京贸国际城'})
#
# # print(data['户型图_1']['户型图内容'])
# with open('图2.jpg','wb') as f:
#     f.write(data['户型图_2']['户型图内容'])

# gridfs方式
# # 存储酷家乐信息
# from gridfs import *
# client = pymongo.MongoClient('127.0.0.1', 27017)
# db = client['kujiele_huxingtu']
# coll = db['huxingtu_0906']
# fs = GridFS(db, collection="huxingtu_images") #连接collection
# for datas in coll.find(no_cursor_timeout=True):
#     id = datas['_id']
#     print(id)
#     for (key,value) in datas.items():
#         if key.startswith('户型图'):
#             pic_href = value['户型图链接'].split('@')[0]
#             print(pic_href)
#             if 'http' in pic_href:
#                 time.sleep(0.5)
#                 img_content = requests.get(pic_href).content
#             else:
#                 img_content = None
#             fs.put(img_content,pic_href=pic_href)

# 导出

from gridfs import *
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['kujiale_huxingtu']
# coll = db['huxingtu_0906']
fs = GridFS(db, collection="huxingtu_images") #连接collection
url = 'https://qhyxpicoss.kujiale.com/fpimgnew/2018/04/13/LLIA5YAKKBBLCIUFAAAAACQ8.jpg'
data = fs.find_one({'pic_href':url})
# print(data)
img = data.read()
with open('图片.jpg','wb') as f:
    f.write(img)


