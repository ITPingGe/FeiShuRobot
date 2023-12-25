#!/usr/bin/env python3
# -*- coding: utf8 -*-
import json
import requests
import settings
from tqdm import tqdm
from poetry import GetPoetry
from datetime import datetime
from weather import get_weather
from movie_calendar import get_cikeee
from requests_toolbelt import MultipartEncoder

LARK_HOST = "https://open.feishu.cn"
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal/"
CHATS = "/open-apis/im/v1/chats"
MESSAGE_URI = "/open-apis/im/v1/messages"
IMG_KEY = "/open-apis/im/v1/images"


def download_file(url, file_name="movie_img.jpg"):
    req = requests.get(url, stream=True)
    data_size = int(req.headers["Content-Length"]) / 1024 / 1024
    with open(file_name, "wb") as f:
        for data in tqdm(iterable=req.iter_content(1024 * 1024), total=data_size, desc=f'正在下载 {file_name}',
                         unit='MB'):
            f.write(data)
    return file_name


def upload_image(img_url):
    url = f"{LARK_HOST}{IMG_KEY}"
    form = {'image_type': 'message',
            'image': (open(download_file(img_url), 'rb'))}  # 需要替换具体的path
    multi_form = MultipartEncoder(form)
    headers = {'Authorization': get_authorization(), 'Content-Type': multi_form.content_type}
    r = requests.request("POST", url, headers=headers, data=multi_form)
    r = json.loads(r.text)
    if r["code"] != 0:
        print(r["msg"])
        return "img_v3_026c_dc0c885d-74ab-4fb2-b9b9-c7ff89364eag"
    return r["data"]["image_key"]


def poetry_card():
    gp = GetPoetry()
    return {
        "poetry_title": gp.title,
        "poetry_dynastic_author": f"[{gp.dynasty}] {gp.author_name}",
        "poetry_content": gp.content,
        "poetry_translation": gp.translation,
        "poetry_link": gp.poetry_link
    }


def movie_card():
    movie_info = get_cikeee()
    return {
        "movie_img": upload_image(movie_info[4]),
        "movie_title": movie_info[8],
        "movie_text": movie_info[7],
        "movie_info": movie_info[6],
        "movie_link": movie_info[5],
        "weather_info": get_weather(settings.get_gaode_key(), 110108),
        "day_text": movie_info[3],
        "today": datetime.now().strftime('%Y 年 %m 月 %d 日')
    }


def message_card():
    current_time = datetime.now()  # 获取当前时间
    hour = current_time.hour  # 提取小时和分钟
    minute = current_time.minute
    if hour == 7 and 30 >= minute >= 0:
        template_variable = movie_card()
        card_id = "MOVIE_CARD"
    else:
        template_variable = poetry_card()
        card_id = "POETRY_CARD"
    return {
        "type": "template",
        "data": {
            "template_id": settings.get_card_id(card_id),
            "template_variable": template_variable
        }
    }


def message_send(event, context):
    """给所有机器人所在的群组发送消息"""
    content = json.dumps(message_card())
    for chat_id in get_chat_id():
        url = f"{LARK_HOST}{MESSAGE_URI}"
        params = (
            ('receive_id_type', 'chat_id'),
        )
        data = json.dumps({
            "receive_id": chat_id,
            "content": content,
            "msg_type": "interactive"
        })
        headers = {
            'Authorization': get_authorization(),
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = requests.post(url=url, headers=headers, data=data, params=params)
        print(response.text)


def get_authorization():
    """获取tenant_access_token"""
    url = f"{LARK_HOST}{TENANT_ACCESS_TOKEN_URI}"
    payload = json.dumps({
        "app_id": settings.get_appid(),
        "app_secret": settings.get_app_secret()
    })
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url=url, headers=headers, data=payload)
    tenant_access_token = json.loads(response.text)["tenant_access_token"]
    print(tenant_access_token)
    return "Bearer {}".format(tenant_access_token)


def get_chats_info(page_token):
    """获取机器人所在的群"""
    url = f"{LARK_HOST}{CHATS}"
    headers = {
        'Authorization': get_authorization(),
    }
    params = (
        ('user_id_type', 'open_id'),
        ('page_token', page_token),
        ('page_size', '10'),
    )
    response = requests.get(url=url, headers=headers, params=params)
    return json.loads(response.text)["data"]


def get_chat_id():
    """获取机器人所在的群的ID"""
    chat_id_list = []
    page_token = ''
    while len(get_chats_info(page_token)["page_token"]) > 0:
        items = get_chats_info(page_token)["items"]
        page_token = get_chats_info(page_token)["page_token"]
        for item in items:
            chat_id = item["chat_id"]
            chat_id_list.append(chat_id)
    else:
        items = get_chats_info(page_token)["items"]
        for item in items:
            chat_id = item["chat_id"]
            chat_id_list.append(chat_id)
    return chat_id_list


if __name__ == '__main__':
    message_send(event=None, context=None)
    # print(uploadImage("https://www.cikeee.cc/uploads/movimg/521/104d/674190152727624.jpg"))
