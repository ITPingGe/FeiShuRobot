#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import requests
import json
from GetGuShiCi import GetGushici

# 腾讯云环境变量
APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")
# LARK_HOST = os.environ.get("LARK_HOST")

# 腾讯云环境变量可以注释掉，用下边这俩
# APP_ID = "*********************"
# APP_SECRET = "*********************"
LARK_HOST = "https://open.feishu.cn"
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal/"
CHATS = "/open-apis/im/v1/chats"
MESSAGE_URI = "/open-apis/im/v1/messages"

"""飞书消息卡片，代码有点low"""
def MessageData():
    GetGuShiCi = GetGushici()
    GetGuShiCi.GetObjectIdList()
    GetGuShiCi.GetBody()
    return {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "content": "%s" % GetGuShiCi.GetTitle(),
                "tag": "plain_text"
            }
        },
        "i18n_elements": {
            "zh_cn": [{
                    "fields": [{
                        "is_short": True,
                        "text": {
                            "content": "**[%s]%s**" % (GetGuShiCi.GetDynasty(), GetGuShiCi.GetAuthorName()),
                            "tag": "lark_md"
                        }
                    }],
                    "tag": "div"
                },
                {
                    "tag": "markdown",
                    "content": "\n%s" % GetGuShiCi.GetContent()
                },
                {
                    "tag": "markdown",
                    "content": "\n**译文：**\n%s" % GetGuShiCi.GetTranslation()
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [{
                        "tag": "plain_text",
                        "content": "每日诗词鉴赏"
                    }]
                }
            ]
        }
    }

"""给所有机器人所在的群组发送消息"""
def MessageSend(event, context):
    content = json.dumps(MessageData())
    for chat_id in GetChatID():
        url = "{}{}".format(LARK_HOST, MESSAGE_URI)
        params = (
            ('receive_id_type', 'chat_id'),
        )
        data = json.dumps({
            "receive_id": chat_id,
            "content": content,
            "msg_type": "interactive"
        })
        headers = {
            'Authorization': GetAuthorization(),
            'Content-Type': 'application/json; charset=utf-8'
        }
        requests.post(url, headers=headers, data=data, params=params)

"""获取tenant_access_token"""
def GetAuthorization():
    url = "{}{}".format(LARK_HOST, TENANT_ACCESS_TOKEN_URI)
    payload = json.dumps({
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url=url, headers=headers, data=payload)
    tenant_access_token = json.loads(response.text)["tenant_access_token"]
    return "Bearer {}".format(tenant_access_token)

"""获取机器人所在的群"""
def GetChatsInfo(page_token):
    url = "{}{}".format(LARK_HOST, CHATS)
    headers = {
        'Authorization': GetAuthorization(),
    }
    params = (
        ('user_id_type', 'open_id'),
        ('page_token', page_token),
        ('page_size', '10'),
    )
    response = requests.get(url=url, headers=headers, params=params)
    return json.loads(response.text)["data"]

"""获取机器人所在的群的ID"""
def GetChatID():
    chat_id_list = []
    page_token = ''
    while len(GetChatsInfo(page_token)["page_token"]) > 0:
        items = GetChatsInfo(page_token)["items"]
        page_token = GetChatsInfo(page_token)["page_token"]
        for item in items:
            chat_id = item["chat_id"]
            chat_id_list.append(chat_id)
    else:
        items = GetChatsInfo(page_token)["items"]
        for item in items:
            chat_id = item["chat_id"]
            chat_id_list.append(chat_id)
    return chat_id_list

if __name__ == '__main__':
    MessageSend(event=None, context=None)