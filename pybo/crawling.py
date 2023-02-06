"""
파일명 : crawling.py
설 명 : 
생성일 : 2023-02-03
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""

from bs4 import BeautifulSoup
import requests


class Crawler:
    def cgv_crawling(self):
        url = "http://www.cgv.co.kr/movies/?lt=1&ft=0"
        response = requests.get(url)

        img_url_list = []
        title_list = []
        percent_list = []

        if response.status_code == 200:
            try:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                li_list = soup.select('ol>li')
                for li in li_list:
                    if li.text:
                        img_url = li.select_one("img").get("src")
                        img_url_list.append(img_url)

                        title = li.select_one("strong.title").getText()
                        title_list.append(title)

                        percent = li.select_one("strong.percent>span").getText()
                        percent_list.append(percent)
            except Exception as e:
                print("="*100)
                print(e)
                print("="*100)

        zipped = zip(img_url_list, title_list, percent_list)
        list_data = list(zipped)
        print(list_data)


def main():
    crawler = Crawler()
    crawler.cgv_crawling()


main()
