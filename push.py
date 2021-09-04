# -*- coding: utf8 -*-
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import os

"""消息推送代码"""
http = requests

wxBotKey = os.environ.get('QYWX_KEY')
sendDingSecret = os.environ.get('DD_BOT_SECRET')
sendDingAccess_token = os.environ.get('DD_BOT_TOKEN')
sendWxCorpid = os.environ.get('QYWX_AM'.split(',')[0])
sendWxCorpsecret = os.environ.get('QYWX_AM'.split(',')[1])
sendWxAgentid = os.environ.get('QYWX_AM'.split(',')[2])
sendTgToken = os.environ.get('TG_BOT_TOKEN')
sendTgChat_id = os.environ.get('TG_USER_ID')


def wxBot(content):
    """
    企业微信机器人消息推送
    """
    if len(content.encode("unicode_escape")) >= 4096:
        msgtype = 'text'
    else:
        msgtype = 'markdown'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
    params = {
        'key': wxBotKey,
        'debug': '1'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "msgtype": msgtype,
        msgtype: {
            "content": content
        }
    }
    r = requests.post(url, headers=headers, params=params, json=data).json()
    return r


def sendDing(content):
    """
    钉钉消息推送
    """
    try:
        timestamp = str(round(time.time() * 1000))
        secret = sendDingSecret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        s = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = 'https://oapi.dingtalk.com/robot/send'
        params = {
            'access_token': sendDingAccess_token,
            'timestamp': timestamp,
            'sign': s
        }
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        res = http.post(url, params=params, json=data)
        res.encoding = 'utf-8'
        res = res.json()
        return 'dingTalk push : ' + res['errmsg']
    except Exception as e:
        return '钉钉机器人推送异常，原因为: ' + str(e)


def sendWx(content):
    """微信企业版消息推送，m为消息参数"""
    params = {
        'corpid': sendWxCorpid,
        'corpsecret': sendWxCorpsecret,
        'agentid': sendWxAgentid,
        'text': content
    }

    http.get('https://api.htm.fun/api/Wechat/text/', params=params)


def sendTg(content):
    try:
        token = '1245607115:AAG7uBbOGIDVGqTAo09vRAkVWcYlTukOzXQ'
        chat_id = '1036459749'
        data = {
            'UnicomTask每日报表': content
        }
        content = urllib.parse.urlencode(data)
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': content
        }
        resp = http.post(url, data=data, params=params)
        if resp.status_code == 200:

            print(resp.text)
        else:
            print(resp.status_code)
    except Exception as e:
        print('Tg通知推送异常，原因为: ' + str(e))
