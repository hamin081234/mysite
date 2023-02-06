import datetime
import unittest
import logging
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import config.wsgi

from django.test import TestCase

from selenium import webdriver
import time
from selenium.webdriver.common.by import By

from pybo.models import Question
from django.utils import timezone

import pyperclip  # 클립 보드를 쉽게 활용할 수 있게 해주는 모듈
from selenium.webdriver.common.keys import Keys  # Ctrl + c, Ctrl + v

# Create your tests here.


class Crawling(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox(executable_path="C:/BIG_AI0102/01_PYTHON/app/geckodriver.exe")
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

    def test_selenium(self):

        #FireFox 웹 드라이버 객체에게 GET을 통하여 네이버의 http요청을 하게 함.
        self.browser.get("http://127.0.0.1:8000/pybo/8/")
        print("self.browser.title:{}".format(self.browser.title))
        self.assertIn("Title", self.browser.title)

        content_textarea = self.browser.find_element(By.ID, 'content')
        content_textarea.send_keys("아무거나 넣어야지")

        button = self.browser.find_element(By.NAME, 'submit_answer')
        # button.submit()
        button.click()

    def test_search_naver(self):
        self.browser.get("https://www.naver.com/")
        search_text = self.browser.find_element(By.ID, 'query')
        search_text.send_keys("강아지")

        search_btn = self.browser.find_element(By.ID, 'search_btn')
        search_btn.click()

        pass

    def test_login_naver(self):
        self.browser.get("https://www.naver.com/")
        account_box = self.browser.find_element(By.ID, 'account')
        login_btn = account_box.find_element(By.TAG_NAME, 'a')
        login_btn.click()

        input_id = self.browser.find_element(By.ID, 'id')
        input_pw = self.browser.find_element(By.ID, 'pw')

        input_id.send_keys("drantfarm82")
        input_pw.send_keys("(HamK)2258!")

        submit_btn = self.browser.find_element(By.ID, 'log.login')
        submit_btn.click()

    def test_clipboard_naver(self):
        user_id = "drantfarm82"
        user_pw = "(HamK)2258!"

        self.browser.get("https://www.naver.com/")
        account_box = self.browser.find_element(By.ID, 'account')
        login_btn = account_box.find_element(By.TAG_NAME, 'a')
        login_btn.click()

        # id
        input_id = self.browser.find_element(By.ID, 'id')
        input_id.click()
        # 클립보드로 copy
        pyperclip.copy(user_id)
        input_id.send_keys(Keys.CONTROL, 'v')  # 클립보드에서 id textinput으로 copy
        time.sleep(1)

        # 비밀번호
        input_pw = self.browser.find_element(By.ID, 'pw')
        input_pw.click()
        # 클립보드로 copy
        pyperclip.copy(user_pw)
        input_pw.send_keys(Keys.CONTROL, 'v')  # mac 은 Keys.COMMAND
        time.sleep(1)

        #로그인 버튼
        login_btn = self.browser.find_element(By.ID, 'log.login')
        login_btn.click()


    def test_paging(self):
        for i in range(500):
            q = Question(subject='금요일 입니다. [%3d]' % i, content='즐거운 금요일!', create_date=timezone.now())
            q.save()

