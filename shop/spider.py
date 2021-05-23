import os, django
import sys

path = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
# print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower.settings")  # project_name 项目名称
django.setup()

import schedule

import requests
import re
import json
import time
from bs4 import BeautifulSoup
import traceback
import ast

from django.db.models import Q
from shop import models
import traceback


# 定义函数抓取每页前30条商品信息
def crow_first(n, key):
    # 构造每一页的url变化
    url = 'https://search.jd.com/Search?keyword=' + key + '&enc=utf-8&page=' + str(2 * n - 1)
    print(url)
    head = {'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=4&s=84&scrolling=y&log_id=1529828108.22071&tpl=3_M&show_items=7651927,7367120,7056868,7419252,6001239,5934182,4554969,3893501,7421462,6577495,26480543553,7345757,4483120,6176077,6932795,7336429,5963066,5283387,25722468892,7425622,4768461',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            }
    r = requests.get(url, headers=head, verify=False)
    # print(r.text)
    # 指定编码方式，不然会出现乱码
    r.encoding = 'utf-8'
    html1 = BeautifulSoup(r.text, 'html.parser')
    # 定位到每一个商品标签li
    datas = html1.select('li.gl-item')
    # print(datas)
    for data in datas:
        try:
            time.sleep(1)
            dicts1 = {}
            p_price = data.select('div > div.p-price > strong > i')
            if len(p_price) == 0:
                p_price = data.select('div > div.p-price > strong > data-price')
            p_price = p_price[0].text.strip()
            dicts1['price'] = p_price
            name = data.select('div.p-name.p-name-type-2  em')[0].text.strip()
            dicts1['name'] = name
            lianjie = data.select('div.p-commit > strong > a')[0].attrs.get('href')
            if 'https' not in lianjie:
                lianjie = 'https:' + lianjie
            dicts1['url'] = lianjie
            shopname = data.select('a.curr-shop.hd-shopname')[0].text.strip()
            dicts1['shopname'] = shopname
            id = re.findall('(\d+).html', lianjie)[0]
            html = requests.get(url=lianjie, headers=head, verify=False)
            soup = BeautifulSoup(html.text, 'html.parser')
            print(lianjie)
            imgs = re.findall('imageList: (\[.*?\])', html.text)
            imgs = ast.literal_eval(imgs[0])
            imgs_url = 'https://img12.360buyimg.com/n4/' + imgs[0]
            dicts1['imgs_url'] = imgs_url

            das = soup.select('div.crumb.fl.clearfix > div')

            pinbai = das[-3].text.strip()

            xinghao = das[-1].text.strip()

            dicts1['pinbai'] = pinbai

            dicts1['xinghao'] = xinghao

            lis = soup.select('ul.parameter2.p-parameter-list > li')
            xinxis = []
            for li in lis:
                xinxis.append(li.text.strip())

            cicun = ''
            for xinxi in xinxis:
                if '屏幕尺寸' in str(xinxi).lower():
                    cicun = str(xinxi).split('：')[-1]
                    break
            dicts1['cicun'] = cicun

            yanse = soup.select('div#choose-attr-1 > div.dd')[0].text.strip().replace('\n', ' ')
            dicts1['yanse'] = yanse

            cpu = ''
            for xinxi in xinxis:
                if '处理器' in str(xinxi).lower():
                    cpu = str(xinxi).split('：')[-1]
                    break
            dicts1['cpu'] = cpu

            leixing = ''
            for xinxi in xinxis:
                if '类型' in str(xinxi).lower():
                    leixing = str(xinxi).split('：')[-1]
                    break
            dicts1['leixing'] = leixing

            neicun = ''
            for xinxi in xinxis:
                if '内存容量' in str(xinxi).lower():
                    neicun = str(xinxi).split('：')[-1]
                    break
            dicts1['neicun'] = neicun

            xitong = ''
            for xinxi in xinxis:
                if '系统' in str(xinxi).lower():
                    xitong = str(xinxi).split('：')[-1]
                    break
            dicts1['xitong'] = xitong

            cangdi = ''
            for xinxi in xinxis:
                if '商品产地' in str(xinxi).lower():
                    cangdi = str(xinxi).split('：')[-1]
                    break
            dicts1['cangdi'] = cangdi

            caizhi = ''
            for xinxi in xinxis:
                if '机身材质' in str(xinxi).lower():
                    caizhi = str(xinxi).split('：')[-1]
                    break
            dicts1['caizhi'] = caizhi

            print(dicts1)

            if not models.Case_item.objects.filter(name=dicts1['name']).filter(lianjie=dicts1['url']):
                models.Case_item.objects.create(
                    name=dicts1['name'],
                    xinghao=dicts1['xinghao'],
                    lianjie=dicts1['url'],
                    image=dicts1['imgs_url'],
                    price=dicts1['price'],
                    text='',
                    pingpai=dicts1['pinbai'],
                    cpu=dicts1['cpu'],
                    leixing=dicts1['leixing'],
                    neicun=dicts1['neicun'],
                    xitong=dicts1['xitong'],
                    cangdi=dicts1['cangdi'],
                    caizhi=dicts1['caizhi'],
                    yanse=dicts1['yanse']
                )
        except:
            print(traceback.format_exc())


# 定义函数抓取每页后30条商品信息
def crow_last(n, key):
    # 获取当前的Unix时间戳，并且保留小数点后5位
    a = time.time()
    b = '%.5f' % a
    url = 'https://search.jd.com/s_new.php?keyword=' + key + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + key + '&cid2=653&cid3=655&page=' + str(
        2 * n) + '&s=' + str(48 * n - 20) + '&scrolling=y&log_id=' + str(b)
    head = {'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            # 'Cookie': 'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'

            }
    r = requests.get(url, headers=head, verify=False)
    # print(r.text)
    # 指定编码方式，不然会出现乱码
    r.encoding = 'utf-8'
    html1 = BeautifulSoup(r.text, 'html.parser')
    # 定位到每一个商品标签li
    datas = html1.select('li.gl-item')
    # print(datas)
    for data in datas:
        try:
            time.sleep(1)
            dicts1 = {}
            p_price = data.select('div > div.p-price > strong > i')
            if len(p_price) == 0:
                p_price = data.select('div > div.p-price > strong > data-price')
            p_price = p_price[0].text.strip()
            dicts1['price'] = p_price
            name = data.select('div.p-name.p-name-type-2  em')[0].text.strip()
            dicts1['name'] = name
            lianjie = data.select('div.p-commit > strong > a')[0].attrs.get('href')
            if 'https' not in lianjie:
                lianjie = 'https:' + lianjie
            dicts1['url'] = lianjie
            shopname = data.select('a.curr-shop.hd-shopname')[0].text.strip()
            dicts1['shopname'] = shopname
            id = re.findall('(\d+).html', lianjie)[0]
            html = requests.get(url=lianjie, headers=head, verify=False)
            soup = BeautifulSoup(html.text, 'html.parser')
            print(lianjie)
            imgs = re.findall('imageList: (\[.*?\])', html.text)
            imgs = ast.literal_eval(imgs[0])
            imgs_url = 'https://img12.360buyimg.com/n4/' + imgs[0]
            dicts1['imgs_url'] = imgs_url

            das = soup.select('div.crumb.fl.clearfix > div')

            pinbai = das[-3].text.strip()

            xinghao = das[-1].text.strip()

            dicts1['pinbai'] = pinbai

            dicts1['xinghao'] = xinghao

            lis = soup.select('ul.parameter2.p-parameter-list > li')
            xinxis = []
            for li in lis:
                xinxis.append(li.text.strip())

            cicun = ''
            for xinxi in xinxis:
                if '屏幕尺寸' in str(xinxi).lower():
                    cicun = str(xinxi).split('：')[-1]
                    break
            dicts1['cicun'] = cicun

            yanse = soup.select('div#choose-attr-1 > div.dd')[0].text.strip().replace('\n', ' ')
            dicts1['yanse'] = yanse

            cpu = ''
            for xinxi in xinxis:
                if '处理器' in str(xinxi).lower():
                    cpu = str(xinxi).split('：')[-1]
                    break
            dicts1['cpu'] = cpu

            leixing = ''
            for xinxi in xinxis:
                if '类型' in str(xinxi).lower():
                    leixing = str(xinxi).split('：')[-1]
                    break
            dicts1['leixing'] = leixing

            neicun = ''
            for xinxi in xinxis:
                if '内存容量' in str(xinxi).lower():
                    neicun = str(xinxi).split('：')[-1]
                    break
            dicts1['neicun'] = neicun

            xitong = ''
            for xinxi in xinxis:
                if '系统' in str(xinxi).lower():
                    xitong = str(xinxi).split('：')[-1]
                    break
            dicts1['xitong'] = xitong

            cangdi = ''
            for xinxi in xinxis:
                if '商品产地' in str(xinxi).lower():
                    cangdi = str(xinxi).split('：')[-1]
                    break
            dicts1['cangdi'] = cangdi

            caizhi = ''
            for xinxi in xinxis:
                if '机身材质' in str(xinxi).lower():
                    caizhi = str(xinxi).split('：')[-1]
                    break
            dicts1['caizhi'] = caizhi

            print(dicts1)

            if not models.Case_item.objects.filter(name=dicts1['name']).filter(lianjie=dicts1['url']):
                models.Case_item.objects.create(
                    name=dicts1['name'],
                    xinghao=dicts1['xinghao'],
                    lianjie=dicts1['url'],
                    image=dicts1['imgs_url'],
                    price=dicts1['price'],
                    text='',
                    pingpai=dicts1['pinbai'],
                    cpu=dicts1['cpu'],
                    leixing=dicts1['leixing'],
                    neicun=dicts1['neicun'],
                    xitong=dicts1['xitong'],
                    cangdi=dicts1['cangdi'],
                    caizhi=dicts1['caizhi'],
                    yanse=dicts1['yanse']
                )
        except:
            print(traceback.format_exc())


def start():
    for key in ['笔记本']:
        for i in range(1, 10):
            # 下面的print函数主要是为了方便查看当前抓到第几页了
            try:
                crow_first(i, key)
            except Exception as e:
                print(traceback.format_exc())
            try:
                crow_last(i, key)
            except Exception as e:
                print(traceback.format_exc())


if __name__ == '__main__':
    start()
