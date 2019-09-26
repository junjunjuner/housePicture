# -*- encoding: utf-8 -*-
'''
Created on $(DATE)

@author: jnnr

@requirments: Pycharm 2019.1; Python 3.5 | Anaconda 3(64-bit)

@decription:图片存储到mongodb数据库
'''
# gridfs方式
# # 存储酷家乐信息
import pymongo
import time
import requests
from gridfs import *
import random
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['kujiale_huxingtu']
# # 读取户型图链接信息
# coll_info = db['huxingtu_info']
# 存储户型图链接
coll_link = db['huxingtu_link']
# for datas in coll_info.find(no_cursor_timeout=True):
#     # id = datas['_id']
#     # print(id)
#     for (key,value) in datas.items():
#         # print(key,value)
#         if key.startswith('户型图'):
#             pic_href = value['户型图链接']
#             print(pic_href)
#             coll_link.insert({'户型图链接':pic_href})
# 存储户型图图片信息
x = 245790
fs = GridFS(db, collection="huxingtu_images") #连接collection
for datas in coll_link.find(no_cursor_timeout=True).skip(x):
    pic_href = datas['户型图链接']
    print(x)
    with open('curtent_num.txt', 'w') as f:
        f.write(str(x) + '\n')
    print(pic_href)
    x = x + 1
    # if x%100 == 0:
    #     time.sleep(random.randint(3,5))
    if not fs.find_one({'pic_href':pic_href}):
        try:
            if 'http' in pic_href:
                try:
                    time.sleep(0.5)
                    img_content = requests.get(pic_href,timeout=1000).content
                except:
                    time.sleep(60)
                    img_content = requests.get(pic_href,timeout=1000).content
            else:
                pic_href = 'https:'+pic_href
                try:
                    time.sleep(0.5)
                    img_content = requests.get(pic_href,timeout=1000).content
                except:
                    with open('fail_url.txt','a') as f:
                        f.write(pic_href + '\n')
                    continue
        except:
            with open('fail_url.txt', 'a') as f:
                f.write(pic_href + '\n')
            with open('fail_num.txt', 'a') as f:
                f.write(str(x) + '\n')
            continue
        fs.put(img_content,pic_href=pic_href)
    else:
        print('已保存哦～',pic_href)
    # for (key,value) in datas.items():
    #     if key.startswith('户型图'):
    #         pic_href = value['户型图链接']
    #         print(pic_href)
    #         if 'http' in pic_href:
    #             time.sleep(0.5)
    #             img_content = requests.get(pic_href).content
    #         else:
    #             img_content = None
    #         fs.put(img_content,pic_href=pic_href)