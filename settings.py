#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import yaml


def config():
    params = yaml.load(open(os.path.join("config.yml"), 'r', encoding='utf-8').read(), Loader=yaml.SafeLoader)
    return params


def get_appid():
    if os.environ.get('APP_ID') is None:
        return config()["ROBOT_INFO"]["APP_ID"]
    else:
        return os.environ.get('APP_ID')


def get_app_secret():
    if os.environ.get('APP_SECRET') is None:
        return config()["ROBOT_INFO"]["APP_SECRET"]
    else:
        return os.environ.get('APP_SECRET')


def get_card_id(card_name):
    if os.environ.get(card_name) is None:
        return config()["CARD_LIST"][card_name]
    else:
        return os.environ.get(card_name)


def get_gaode_key():
    if os.environ.get('GAODE_KEY') is None:
        return config()["GAODE_INFO"]["GAODE_KEY"]
    else:
        return os.environ.get('GAODE_KEY')
