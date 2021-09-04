# -*- coding: utf8 -*-
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import json

"""消息推送代码"""
http = requests

path = os.path.dirname(__file__)
with open(os.path.join(path, 'config.json'), 'r', encoding='utf-8') as f:
    Config = json.load(f)
wxBotKey = Config['wxBot']['Key']
sendDingSecret = Config['sendDing']['Secret']
sendDingAccess_token = Config['sendDing']['Token']
sendWxCorpid = Config['sendWx']['Corpid']
sendWxCorpsecret = Config['sendWx']['Corpsecret']
sendWxAgentid = Config['sendWx']['Agentid']
sendServerKey = Config['sendServer']['Key']
sendPushToken = Config['sendPush']['Token']
sendTgToken = Config['sendTg']['Token']
sendTgChat_id = Config['sendTg']['Chat_id']
WxPusherAppToken = Config['WxPusher']['AppToken']
WxPusherUid = Config['WxPusher']['Uid']


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


def sendEmail(content):
    """
    邮箱消息推送
    """
    mail_host = "smtp.189.cn"
    mail_user = "18555894518@189.cn"
    mail_pass = "Aa199612"
    sender = '18555894518@189.cn'
    receivers = ['1637494149@qq.com']

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(mail_user, 'utf-8')
    message['To'] = Header(receivers[0], 'utf-8')
    subject = '爸爸，通知书来了！'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return "邮件发送成功"
    except smtplib.SMTPException as e:
        return f"Error: 无法发送邮件，因为：{str(e)}"


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


def sendServer(content):
    url = f'https://sc.ftqq.com/{sendServerKey}1.send'
    params = {
        'text': '您有一个新的消息~',
        'desp': content
    }
    http.get(url, params=params)


def sendPush(content):
    url = f'http://www.pushplus.plus/send?'
    params = {
        'token': sendPushToken,
        'title': '爸爸！你关注的信息更新了哦~~',
        'content': content,
        'template': 'html'
    }
    http.get(url, params=params)


def sendEmail2(content):
    try:
        url = 'http://liuxingw.com/api/mail/api.php'
        params = {
            'address': '1637494149@qq.com',
            'name': '爸爸，录取通知书来了！',
            'certno': content
        }
        r = http.get(url, params=params).json()
        if r['Code'] == '1':
            return '邮件发送成功~'
        else:
            return '邮件发送失败~'
    except Exception as e:
        return f'错误，因为：{str(e)}'


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


def wxpusher(content):
    url = 'http://wxpusher.zjiecode.com/api/send/message/'
    params = {
        "appToken": 'AT_QSdQ5ACI0yxN7uKO6i37nrdkz7sVr2zn',
        "content": content,
        "uid": WxPusherUid
    }
    http.get(url, params=params, headers={'Content-Type': 'application/json'})
