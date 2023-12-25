#!/usr/bin/evn python3
# -*- coding: utf-8
"""
@Project    :   Install_List.py
@File       :   movie_calendar.py
@Author     :   yanweiping
@Date       :   2023/12/21 11:13
"""
import requests
from bs4 import BeautifulSoup

CIKEEE_HOST = "https://www.cikeee.cc/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
HEADERS = {"user-agent": USER_AGENT}


def get_cikeee():
    r = requests.get(url=CIKEEE_HOST, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser", from_encoding="utf-8")
    month = soup.find(attrs={'id': 'month'}).string
    day = soup.find(attrs={'id': 'day'}).string
    week = soup.find(attrs={'id': 'week'}).string
    day_text = soup.find(attrs={'id': 'daytext'}).text.replace("\xa0", "")
    movie_img = soup.find(attrs={'id': 'movie-img'})
    movie_img = CIKEEE_HOST + movie_img.get('src')
    movie_link = soup.find(attrs={'id': 'movie-img-a'})
    movie_link = CIKEEE_HOST + movie_link.get('href')
    movie_information = soup.find(attrs={'id': 'movie-information'}).string
    movie_information = movie_information.replace("\xa0", " ")
    movie_text = soup.find(attrs={'id': 'movie-text'}).string
    movie_name = soup.find(attrs={'id': 'movie-name'}).string.replace("—", "")
    return month, day, week, day_text, movie_img, movie_link, movie_information, movie_text, movie_name


if __name__ == "__main__":
    print(get_cikeee())
