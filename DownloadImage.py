#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent import futures
from hashlib import sha1
from time import sleep
import json
import requests
import os

proxy_list = []

headers = {
    'Access-Control-Request-Method': 'GET',
    'Origin': 'https://crypko.ai',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Access-Control-Request-Headers': 'address,authorization',
}


# def get_proxy():
#     global proxy_list

#     if len(proxy_list) == 0:
#         res = requests.get('http://xxxxxx/get_all').json()
#         proxy_list = res

#     return proxy_list.pop()


def generate_url(crypko):
    salt = 'asdasd3edwasd'
    mes = crypko['noise'] + salt + crypko['attrs']
    return sha1(mes.encode()).hexdigest()


def download(cid):
    global cnt

    url = 'https://img.crypko.ai/daisy/{}_lg.jpg'
    url = url.format(generate_url(crypkos[cid]))
    name = 'Crypko #' + str(crypkos[cid]['id']) + '.jpg'

    if os.path.exists('images/{}/{}'.format(n, name)):
        cnt += 1
        return

    while True:
        try:
            # proxy = get_proxy()
            # res = requests.get(url, proxies={'HTTPS': 'http://' + proxy}, headers=headers, timeout=5).content
            res = requests.get(url, headers=headers, timeout=5).content

            if res[:5] == b'<?xml' and b'Anonymous caller does not have storage.objects.get access' in res:
                res = '此卡不存在'.encode()
            elif not res[:2] == b'\xff\xd8':
                print(crypkos[cid]['id'])
                raise Exception('Not JPG')

            cnt += 1
            print('[{}][{:.2f}%]Download #{}'.format(n, cnt / 500 * 100, crypkos[cid]["id"]))
            with open('images/{}/{}'.format(n, name), 'wb') as f:
                f.write(res)
            break
        except Exception as e:
            print(e)
            print('failed to download #{}, asking for new proxy'.format(crypkos[cid]["id"]))
            # requests.get('http://xxxx/delete?proxy=' + proxy)

if not os.path.exists('./images'):
    os.mkdir('./images')

try:
    i = max(int(i) for i in os.listdir('./images') if i.isdigit())
except ValueError:
    i = 0
# get_proxy() # 初始化代理
while True:

    if not os.path.exists('./images/{}'.format(i)):
        os.mkdir('./images/{}'.format(i))
    n = i

    with open('./new_data/{}'.format(i), 'r') as f:
        crypkos = json.load(f)

    cnt = 0
    with futures.ThreadPoolExecutor(max_workers=25) as executor:
        tasks = executor.map(download, range(0, 500))

        for _ in tasks:
            pass

    if not os.path.exists('./new_data/{}'.format(i + 1)):
        print('no new cards, sleeping for 60s')
        sleep(60)
        continue
    else:
        print('finish, sleeping for 5s...')
        sleep(5)
        i += 1
