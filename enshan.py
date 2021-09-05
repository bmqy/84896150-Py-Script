#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
说明: 环境变量名`KXDAO_COOKIE`
cron: 25 7 * * *
new Env('恩山论坛-签到');
"""
import requests
import os
import push
import re

h = requests.Session()


def run(cook):
    msg = ''
    url = 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Cookie': cook
    }
    resp = h.get(url, headers=headers)
    try:

        bi = re.findall('恩山币: </em>(.*?)nb &nbsp;', resp.text)[0]
        jf = re.findall('<em>积分: </em>(.*?)<span', resp.text)[0]
        msg += f'恩山币：{bi}\n积分：{jf}\n'
        return msg
    except Exception as e:
        msg += f'{str(e)}\n'
        return msg


def main():
    cook = os.environ.get('ENSHAN_COOKIE')
    m = f'===恩山论坛开始===\n{run(cook)}===恩山论坛结束===\n'
    print(m)
    push.sendDing(m)
    push.wxBot(m)
    push.sendWx(m)


if __name__ == '__main__':
    main()
