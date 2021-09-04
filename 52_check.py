# -*- coding: utf8 -*-
"""
cron: 25 20 * * *
new Env('吾爱签到');
"""
import requests
import re
import os
# from push import wxBot

h = requests.Session()


def main(cookie):
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    h.cookies.update(cookie_dict)
    msg = ''
    url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.18 Mobile Safari/537.36',
        'ContentType': 'text/html;charset=gbk'
    }
    check_url = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
    h.get(url, headers=headers)
    r = h.get(check_url, headers=headers).text
    try:
        qd = re.findall('<p>(.*?)</p>', r)[0]
        msg += f'签到结果：{qd}\n'
    except Exception as e:
        msg += f'{str(e)}\n'
        return msg
    i_url = 'https://www.52pojie.cn/home.php?mod=spacecp&ac=credit&showcredit=1'
    i_r = h.get(i_url, headers=headers).text
    try:
        cb = re.findall('吾爱币: </em>(.*?) CB &nbsp', i_r)[0]
        jf = re.findall('积分: </em>(.*?) <span', i_r)[0]
        msg += f'当前吾爱币：{cb}，积分：{jf}\n'
        return msg
    except Exception as e:
        msg += f'{str(e)}\n'
        return msg


if __name__ == '__main__':
    Cookie = os.environ.get('52_CK')
    print(main(Cookie))
