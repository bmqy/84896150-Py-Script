# -*- coding: utf8 -*-
"""
cron: 25 2 * * *
new Env('恩山论坛-签到');
"""
import requests
import os
from push import sendDing
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

        bi = re.findall('恩山币: </em>(.*?)nb &nbsp;', resp.text)
        jf = re.findall('<em>积分: </em>(.*?)<span', resp.text)
        msg += f'恩山币：{bi}\n积分：{jf}\n'
        return msg
    except Exception as e:
        msg += f'{str(e)}\n'
        return msg


def main():
    cook = os.environ.get('ENSHAN_COOKIE')
    sendDing(f'===恩山论坛开始===\n{run(cook)}===恩山论坛结束===\n')


if __name__ == '__main__':
    main()
