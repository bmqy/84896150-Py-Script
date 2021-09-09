#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
cron: */15 * * * *
new Env('科技玩家-签到');
"""
import requests
from push import send


def login(usr, pwd):
    session = requests.Session()
    msg = ''
    login_url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'
    }
    data = {
        'nickname': '',
        'username': usr,
        'password': pwd,
        'code': '',
        'img_code': '',
        'invitation_code': '',
        'token': '',
        'smsToken': '',
        'luoToken': '',
        'confirmPassword': '',
        'loginType': ''
    }
    res = session.post(login_url, headers=headers, data=data)
    if res.status_code == 200:
        status = res.json()
        msg += f"账号`{status.get('name')}`登陆成功\n"
        msg += f"ID：{status.get('id')}\n"
        msg += f"金币：{status.get('credit')}\n"
        msg += f"等级：{status.get('lv').get('lv').get('name')}\n"
        token = status.get('token')
        check_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
        check_head = {
            'authorization': f'Bearer {token}'
        }
        resp = session.post(check_url, headers=check_head)
        if resp.status_code == 200:
            info = resp.json()
            if type(info) == dict:
                msg += f"签到成功：{info.get('credit')}金币\n"
            else:
                msg += f"已经签到：{info}金币\n"
        return msg
    else:
        msg += '账号登陆失败\n账号或密码错误\n'
        return


if __name__ == '__main__':
    m = login('1637494149@qq.com', 'Aa199612')
    print(m)
    send(m)

