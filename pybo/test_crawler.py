"""
파일명 : ${FILE_NAME}
설 명 : 
생성일 : 2023-01-31
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""
from unittest import TestCase

from pybo.crawler import Crawler


def main():
    pass


main()


class TestCrawler(TestCase):
    def test_parse_html(self):
        self.fail()

    def test_find_product_list(self):
        self.fail()

    def test_product_info_parse(self):
        crawler = Crawler()
        url = "https://www.iloom.com/product/detail.do?productCd=HB722501"
        product_detail = crawler.parse_html(url)
        crawler.product_info_parse(product_detail)
