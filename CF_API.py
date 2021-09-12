#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
cron: */15 * * * *
new Env('域名解析');
"""
import requests
import time
import json
import os
from push import send

http = requests.Session()


def askApi(accountInfo, dnsInfo):
    global lsip
    t = time.strftime("%H时%M分%S秒", time.localtime())
    msg = ''
    headers = {
        'user-agent': 'Mozilla/5.0',
        'X-Auth-Email': accountInfo['email'],
        'X-Auth-Key': accountInfo['api'],
        'Content-Type': 'application/json'
    }
    http.headers.update(headers)
    url = f'''https://api.cloudflare.com/client/v4/zones/{accountInfo['zones']}/dns_records'''
    resp = http.get(url, headers=headers)
    try:
        List = resp.json()['result']
        for x in List:
            if x['id'] == dnsInfo['dns_records']:
                lsip = x['content']
                if x['content'] == dnsInfo['content']:
                    msg += f'''=====无需解析=====\n时间：{t}\n域名：{dnsInfo['name']}\n本次IP：{dnsInfo['content']}\n记录IP：{x['content']}'''
                    print(msg)
                    return True
    except:
        msg += f'''=====解析失败=====\n时间：{t}\n域名：{dnsInfo['name']}解析失败❗'''
        return msg
    apiUrl = f'''https://api.cloudflare.com/client/v4/zones/{accountInfo['zones']}/dns_records/{dnsInfo['dns_records']}'''
    dnsInfo.pop('dns_records')
    body = json.dumps(dnsInfo)

    res = http.put(apiUrl, data=body)
    if res.status_code == 200:
        msg += f'''=====解析成功！=====\n时间：{t}\n域名：{dnsInfo['name']}\n解析IP：{dnsInfo['content']}\n历史IP：{lsip}'''
        print(msg)
        return msg
    else:
        msg += f'''=====解析失败=====\n时间：{t}\n域名：{dnsInfo['name']}解析失败\n本次IP：{dnsInfo['content']}'''
        print(msg)
        return msg


if __name__ == '__main__':
    ipv4 = requests.get("http://ip.3322.net/").text
    ipv4 = ipv4[:-1]
    if 'CF_EMAIL' in os.environ and os.environ['CF_EMAIL'] and 'CF_KEY' in os.environ and os.environ['CF_KEY'] and \
            'CF_ZONES' in os.environ and os.environ['CF_ZONES'] and 'CF_DOMAIN' in os.environ and os.environ[
        'CF_DOMAIN'] \
            and 'CF_DNS' in os.environ and os.environ['CF_DNS']:
        email = os.environ['CF_EMAIL']
        api = os.environ['CF_KEY']
        zones = os.environ['CF_ZONES']
        name = os.environ['CF_DOMAIN']
        dns_records = os.environ['CF_DNS']
        accountInfo = {
            'email': email,
            'zones': zones,
            'api': api
        }
        dnsInfo = {
            'dns_records': dns_records,  # DNS解析ID
            'type': 'A',  # A 记录
            'name': name,  # 解析的域名
            'content': ipv4,  # ipv4地址
            'ttl': 1,  # TTL
            'proxied': False  # 是否开启Cloudflare
        }
        M = askApi(accountInfo, dnsInfo=dnsInfo)
        if M:
            send('域名解析', M)
    else:
        send('域名解析', '未正确配置环境变量')
