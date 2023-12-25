# -*- coding: utf-8 -*-
import requests
import json
import random

HTTP = "http://"
HTTPS = "https://"
HOST = "avoscloud.com"
XI_CHUANG_ZHU_HOST = "m.xichuangzhu.com"
SELECTED_LISTS = "/1.1/call/getSelectedLists"
LIST_WORKS = "/1.1/call/getListWorks"
POETRY_DETAIL = "/work/"


def headers():
    return {
        'content-type': 'application/json;charset=UTF-8',
        'x-lc-id': '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
        'x-lc-sign': 'bef0d00c0285f26dd69d3aa201890cbb,1673528504681'
    }


def get_obj_id_list():
    obj_id_list = []
    data = json.dumps({"page": random.randint(0, 9), "perPage": 100})
    r = requests.post(url=HTTPS + HOST + SELECTED_LISTS, headers=headers(), data=data)
    r = json.loads(r.text)
    if len(r["result"]) > 0:
        for i in range(0, len(r["result"])):
            obj_id = r["result"][i]["objectId"]
            obj_id_list.append(obj_id)
    return obj_id_list


def get_poetry_list():
    obj_id_list = get_obj_id_list()
    while True:
        data = json.dumps({
            "listId": obj_id_list[random.randint(0, len(obj_id_list) - 1)],
            "page": random.randint(0, 9),
            "perPage": 100
        })
        r = requests.post(url=HTTPS + HOST + LIST_WORKS, headers=headers(), data=data)
        r = json.loads(r.text)
        if len(r["result"]) > 0:
            return r


class GetPoetry:
    def __init__(self):
        self.body: dict = get_poetry_list()
        self.place: int = random.randint(0, len(self.body["result"]) - 1)
        self.show_order = self.body["result"][self.place]["showOrder"]
        self.kind_cn = self.body["result"][self.place]["work"]["kindCN"]
        self.dynasty = self.body["result"][self.place]["work"]["dynasty"]
        self.author_name = self.body["result"][self.place]["work"]["authorName"]
        self.title = str(self.body["result"][self.place]["work"]["title"])
        self.content = str(self.body["result"][self.place]["work"]["content"])
        self.annotation = str(self.body["result"][self.place]["work"]["annotation"])
        self.translation = str(self.body["result"][self.place]["work"]["translation"])
        if len(self.translation) == 0:
            self.translation = "无"
        self.intro = str(self.body["result"][self.place]["work"]["intro"])
        self.master_comment = str(self.body["result"][self.place]["work"]["masterComment"])
        self.objict_id = str(self.body["result"][self.place]["work"]["objectId"])
        self.poetry_link = f"{HTTP}{XI_CHUANG_ZHU_HOST}{POETRY_DETAIL}{self.objict_id}"


if __name__ == "__main__":
    print(GetPoetry().body)
    print(GetPoetry().content)
