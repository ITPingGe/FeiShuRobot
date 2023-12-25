#!/usr/bin/evn python3
# -*- coding: utf-8
"""
@Project    :   Install_List.py
@File       :   weather.py
@Author     :   yanweiping
@Date       :   2023/12/21 17:39
"""
import json
import requests
import settings

HOST = "https://restapi.amap.com"
WEATHER_PATH = "/v3/weather/weatherInfo"


def get_weather(key, city_code):
    payload = f"?key={key}&extensions=all&city={city_code}"
    url = f"{HOST}{WEATHER_PATH}{payload}"
    r = json.loads(requests.get(url).text)
    city_name = r["forecasts"][0]["province"]
    city_info = r["forecasts"][0]["casts"][0]
    if city_info["dayweather"] == city_info["nightweather"]:
        city_weather = city_info["dayweather"]
    else:
        city_weather = f"{city_info['dayweather']}转{city_info['nightweather']}"
    city_temperature = f"{city_info['nighttemp']}～{city_info['daytemp']}"
    return f"{city_name} {city_weather} {city_temperature}°C"


if __name__ == "__main__":
    print(get_weather(settings.get_gaode_key(), 110108))
