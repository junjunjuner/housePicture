# -*- encoding: utf-8 -*-
'''
Created on $(DATE)

@author: jnnr

@requirments: Pycharm 2019.1; Python 3.5 | Anaconda 3(64-bit)

@decription:房天下楼盘名数据采集
'''

# 测试
import requests
import re
from lxml import etree
page = 1
url = 'https://newhouse.fang.com/house/s/b1saledate-b9%s/'%page
print(url)
req = requests.get(url)
req.encoding = 'gbk'
tree = etree.HTML(req.text)

try:
    otherpage = tree.xpath(".//div[@class='otherpage']/span/text()")[1]
    total_page = re.findall("/(.*?)\xa0",otherpage)[0]
    print(total_page)
except Exception as e:
    print(e)
    print(url)
try:
    # 楼盘数量
    number = tree.xpath(".//a[@id='allUrl']/span/text()")[0][1:-1]
    # 楼盘
    detail_list = tree.xpath(".//div[@class='clearfix']/div[@class='nlc_details']")
    for detail in detail_list:
        # 楼盘名
        build_name = detail.xpath("normalize-space(div[@class='house_value clearfix']/div/a/text())")
        # 开盘时间
        sjina = detail.xpath("normalize-space(div[starts-with(@id,'sjina')]/text())")
        if '开盘时间' not in sjina:
            build_time = None
        else:
            build_time = re.findall("开盘时间：(.*?)",sjina)
except Exception as e:
    print("无法匹配：", e)
    number = 0

