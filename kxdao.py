#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
说明: 环境变量名`KXDAO_COOKIE`
cron: 25 7 * * *
new Env('科学刀-签到');
"""
import requests
import re
import os
from push import send

h = requests.Session()
List = []


def main(cookie):
    h.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'})
    hash_url = 'https://www.kxdao.net/space-uid-74943.html'
    hash_headers = {
        'Host': 'www.kxdao.net',
        'Referer': 'https://www.kxdao.net/plugin.php',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie
    }
    hash_r = h.get(url=hash_url, headers=hash_headers)
    try:
        formhash = re.findall('name="formhash" value="(.*?)" />', hash_r.text)[0]
    except Exception as e:
        List.append(f'{str(e)}')
        return

    check_url = 'https://www.kxdao.net/plugin.php'
    check_params = dict(
        id='dsu_amupper',
        ppersubmit='true',
        formhash=formhash
    )
    check_headers = {
        'referer': 'https://www.kxdao.net/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie
    }
    check_r = h.get(url=check_url, headers=check_headers, params=check_params).text
    try:
        qd = re.findall('<p>(.*?)</p>', check_r)[0]
        List.append(f'签到结果：{qd}')
    except Exception as e:
        List.append(f'{str(e)}')
        return
    i_url = 'https://www.kxdao.net/home.php?mod=spacecp&ac=credit&showcredit=1'
    i_headers = {
        'Host': 'www.kxdao.net',
        'referer': 'https://www.kxdao.net/',
        'Cookie': cookie
    }
    i_r = h.get(url=i_url, headers=i_headers).text

    try:
        db = re.findall('class="xi1 cl"><em> DB: </em>(.*?)&nbsp', i_r)[0]
        jf = re.findall('<li class="cl"><em>积分: </em>(.*?)<span class="xg1">', i_r)[0]
        List.append(f'用户DB：{db[:-2]}，积分{jf}')
    except Exception as e:
        List.append(f'{str(e)}')


if __name__ == '__main__':
    i = 0
    if 'KXDAO_COOKIE' in os.environ:
        users = os.environ['KXDAO_COOKIE'].split('&')
        for x in users:
            i += 1
            List.append(f'===> [账号{str(i)}]Start <===')
            main(x)
            List.append(f'===> [账号{str(i)}]End <===\n')
        tt = '\n'.join(List)
        print(tt)
        send('科学刀', tt)
    else:
        print('未配置环境变量')
        send('科学刀', '未配置环境变量')
