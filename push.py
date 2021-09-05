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


def wxBot(content):
    """
        企业微信机器人消息推送
        """
    wxBotKey = os.environ.get('QYWX_KEY')
    if wxBotKey == '':
        return
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
    sendDingSecret = os.environ.get('DD_BOT_SECRET')
    sendDingAccess_token = os.environ.get('DD_BOT_TOKEN')
    if sendDingSecret or sendDingAccess_token == '':
        return
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
    Wx = os.environ.get('QYWX_AM')
    if Wx == '':
        return
    sendWxCorpid = Wx[0]
    sendWxCorpsecret = Wx[1]
    sendWxAgentid = Wx[2]
    """微信企业版消息推送，m为消息参数"""
    params = {
        'corpid': sendWxCorpid,
        'corpsecret': sendWxCorpsecret,
        'agentid': sendWxAgentid,
        'text': content
    }

    http.get('https://api.htm.fun/api/Wechat/text/', params=params)
