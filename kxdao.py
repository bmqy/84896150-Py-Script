# -*- coding: utf8 -*-
import requests
import re
import os
import push

h = requests.Session()


def main(cookie):
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    h.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'})
    h.cookies.update(cookie_dict)
    msg = ''
    hash_url = 'https://www.kxdao.net/space-uid-74943.html'
    hash_headers = {
        'Host': 'www.kxdao.net',
        'Referer': 'https://www.kxdao.net/plugin.php',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    hash_r = h.get(url=hash_url, headers=hash_headers)
    try:
        formhash = re.findall('name="formhash" value="(.*?)" />', hash_r.text)[0]
    except Exception as e:
        msg += f'{str(e)}'
        return msg

    check_url = 'https://www.kxdao.net/plugin.php'
    check_params = dict(
        id='dsu_amupper',
        ppersubmit='true',
        formhash=formhash
    )
    check_headers = {
        'referer': 'https://www.kxdao.net/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    check_r = h.get(url=check_url, headers=check_headers, params=check_params).text
    try:
        qd = re.findall('<p>(.*?)</p>', check_r)[0]
        msg += f'签到结果：{qd}\n'
    except Exception as e:
        msg += f'{str(e)}'
        return msg
    i_url = 'https://www.kxdao.net/home.php?mod=spacecp&ac=credit&showcredit=1'
    i_headers = {
        'Host': 'www.kxdao.net',
        'referer': 'https://www.kxdao.net/'
    }
    i_r = h.get(url=i_url, headers=i_headers).text

    try:
        db = re.findall('class="xi1 cl"><em> DB: </em>(.*?)&nbsp', i_r)[0]
        jf = re.findall('<li class="cl"><em>积分: </em>(.*?)<span class="xg1">', i_r)[0]
        msg += f'用户DB：{db[:-2]}，积分{jf}\n'
        print(msg)
        return msg
    except Exception as e:
        msg += f'{str(e)}'
        return msg


if __name__ == '__main__':
    Cookie = os.environ.get('KXDAO_COOKIE')
    m = '---科学刀签到开始---\n'
    m += main(Cookie) + '\n'
    m += '---科学刀签到结束---\n'
    push.sendDing(m)
    push.wxBot(m)
    push.sendWx(m)
