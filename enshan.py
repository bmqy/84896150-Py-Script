#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
说明: 环境变量名`ENSHAN_COOKIE`
cron: 25 7 * * *
new Env('恩山论坛-签到');
"""
import requests
import os
from push import send
import re

h = requests.Session()
List = []


def run(cook):
    url = 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Cookie': cook
    }
    resp = h.get(url, headers=headers)
    try:

        bi = re.findall('恩山币: </em>(.*?)nb &nbsp;', resp.text)[0]
        jf = re.findall('<em>积分: </em>(.*?)<span', resp.text)[0]
        List.append(f'恩山币：{bi}\n积分：{jf}')
    except Exception as e:
        List.append(f'{str(e)}')


def main():
    i = 1
    if 'ENSHAN_COOKIE' in os.environ:
        users = os.environ['ENSHAN_COOKIE'].split('&')
        for x in users:
            i += 1
            List.append(f'===账号{str(i)}开始===\n')
            run(x)
        tt = '\n'.join(List)
        print(tt)
        send('恩山论坛', tt)
    else:
        print('未配置环境变量')
        send('恩山论坛', '未配置环境变量')


if __name__ == '__main__':
    main()
