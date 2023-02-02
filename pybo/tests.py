import datetime
import unittest
import logging
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

from django.test import TestCase

# Create your tests here.


class Crawling(unittest.TestCase):
    def setUp(self) -> None:
        logging.info('setUp')

    def tearDown(self) -> None:
        logging.info('tearDown')

    def test_weather(self):
        """ 날씨 """
        now = datetime.datetime.now()
        print("now:{}".format(now))

        # yyyymmdd hh:MM
        newDate = now.strftime("%Y-%m-%d %H:%M:%S")
        print("="*35)
        print(newDate)
        print("="*35)

        # --------------------------------------------------------
        naver_weather_url = "https://weather.naver.com/today/09650108"
        html = urlopen(naver_weather_url)
        print("html:{}".format(html))

        bs_object = BeautifulSoup(html, 'html.parser')
        tmpes = bs_object.find("strong", "current")

        print("현재 서초구 서초동 날씨:{}".format(tmpes.getText()))

        logging.info('test_weather')


