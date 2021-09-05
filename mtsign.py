#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
说明: 环境变量名`MT_INFO`，账号密码-分割
cron: 25 7 * * *
new Env('MT论坛-签到');
"""
import requests
import re
import time
import os
import push

h = requests.Session()


def run(username, password):
    msg = ''
    get_url = 'https://bbs.binmt.cc/k_misign-sign.html'
    get_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    r = h.get(get_url, headers=get_headers)
    try:
        formhash = re.findall('<input type="hidden" name="formhash" value="(.*?)" />', r.text)[0]
    except Exception as e:
        msg += f'{str(e)}'
        return msg
    time.sleep(1)
    hash_url = 'https://bbs.binmt.cc/member.php'
    hash_params = dict(
        mod='logging',
        action='login',
        infloat='yes',
        handlekey='login',
        inajax='1',
        ajaxtarget='fwin_content_login'
    )
    hash_headers = {
        'Host': 'bbs.binmt.cc',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Referer': 'https://bbs.binmt.cc/'
    }
    hash_r = h.get(hash_url, params=hash_params, headers=hash_headers)
    try:
        loginhash = re.findall('amp;loginhash=(.*?)"', hash_r.text)[0]
    except Exception as e:
        msg += f'{str(e)}'
        return msg
    time.sleep(1)
    login_url = 'https://bbs.binmt.cc/member.php'
    login_params = dict(
        mod='logging',
        action='login',
        loginsubmit='yes',
        handlekey='login',
        loginhash=loginhash,
        inajax='1'
    )
    login_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    login_data = {
        'formhash': formhash,
        'referer': 'https://bbs.binmt.cc/',
        'loginfield': 'username',
        'username': username,
        'password': password,
        'questionid': '0',
        'answer': ''
    }
    login_r = h.post(login_url, headers=login_headers, params=login_params, data=login_data)
    if '欢迎您回来' in login_r.text:
        msg += '登陆成功！\n'
    else:
        msg += '登陆失败！\n'
    time.sleep(1)
    print(formhash)
    s_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    s_r = h.get('https://bbs.binmt.cc', headers=s_headers).text
    try:
        s_formhash = re.findall('<input type="hidden" name="formhash" value="(.*?)" />', s_r)[0]
        print(s_formhash)
    except Exception as e:
        msg += f'{str(e)}'
        return msg
    check_url = 'https://bbs.binmt.cc/plugin.php'
    check_params = dict(
        id='k_misign:sign',
        operation='qiandao',
        formhash=s_formhash,
        format='empty',
        inajax='1',
        ajaxtarget='JD_sign'
    )
    check_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Referer': 'https://bbs.binmt.cc/'
    }
    check_r = h.get(check_url, params=check_params, headers=check_headers).text
    print(check_r)
    if '今日已签' in check_r:
        msg += '今天已经签到过了\n'
    elif '签到成功' in check_r:
        msg1 = re.findall('获得随机奖励(.*?)金币', check_r)[0]
        msg2 = re.findall('已累计签到\d+ 天')
        msg += f'签到成功，{msg1}，{msg2}\n'
    else:
        msg += '签到失败，未知错误\n'
        return msg
    i_url = 'https://bbs.binmt.cc/home.php?mod=spacecp&ac=credit&showcredit=1'
    i_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Referer': 'https://bbs.binmt.cc/'
    }
    i_r = h.get(i_url, headers=i_headers).text
    try:
        db = re.findall('金币: </em>(.*?)&nbsp', i_r)[0]
        jf = re.findall('积分: </em>(.*?)<span', i_r)[0]
        msg += f'用户金币：{db}，积分{jf}\n'
        return msg
    except Exception as e:
        msg += f'{str(e)}'
        return msg


def main():
    user = os.environ.get('MT_INFO').split('-')
    username, password = user
    m = '===MT论坛签到开始===\n'
    m += run(username, password)
    m += '===MT论坛签到结束===\n'
    push.sendDing(m)
    push.wxBot(m)
    push.sendWx(m)


if __name__ == '__main__':
    main()
