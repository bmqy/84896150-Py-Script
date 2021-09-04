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
        msg += f"""{xpath(resp.text, '//li[@class="xi1 cl"]/em/text()')[0][1:]}{xpath(resp.text, '//li[@class="xi1 cl"]/text()')[0]}\n"""
        msg += f"""{xpath(resp.text, '//li[@class="cl"]/em/text()')[0]}{xpath(resp.text, '//li[@class="cl"]/text()')[0]}\n"""
        return msg
    except Exception as e:
        msg += f'{str(e)}\n'
        return msg


def main():
    cook = os.environ.get('ENSHAN_COOKIE')
    sendDing(f'===恩山论坛开始===\n{run(cook)}===恩山论坛结束===\n')


if __name__ == '__main__':
    main()
