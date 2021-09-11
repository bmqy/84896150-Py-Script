#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
说明: 环境变量名`WUAI_COOKI`
cron: 25 7 * * *
new Env('吾爱破解-签到');
"""
import requests
import re
import os
from push import send

h = requests.Session()
List = []


def main(cookie):
    url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.18 Mobile Safari/537.36',
        'ContentType': 'text/html;charset=gbk',
        'Cookie': cookie
    }
    check_url = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
    h.get(url, headers=headers)
    r = h.get(check_url, headers=headers).text
    try:
        qd = re.findall('<p>(.*?)</p>', r)[0]
        List.append(f'签到结果：{qd}')
    except Exception as e:
        List.append(f'{str(e)}')
        return
    i_url = 'https://www.52pojie.cn/home.php?mod=spacecp&ac=credit&showcredit=1'
    i_r = h.get(i_url, headers=headers).text
    try:
        cb = re.findall('吾爱币: </em>(.*?) CB &nbsp', i_r)[0]
        jf = re.findall('积分: </em>(.*?) <span', i_r)[0]
        List.append(f'当前吾爱币：{cb}，积分：{jf}')
    except Exception as e:
        List.append(f'{str(e)}')


if __name__ == '__main__':
    i = 1
    if 'WUAI_COOKIE' in os.environ:
        users = os.environ['WUAI_COOKIE'].split('&')
        for x in users:
            i += 1
            List.append(f'===账号{str(i)}开始===\n')
            main(x)
        tt = '\n'.join(List)
        print(tt)
        send('吾爱破解', tt)
    else:
        print('未配置环境变量')
        send('吾爱破解', '未配置环境变量')
