"""
파일명 : ${FILE_NAME}
설 명 : 
생성일 : 2023-01-31
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""
from unittest import TestCase

# from pybo.crawler import Crawler


def main():
    pass


main()


class TestCrawler(TestCase):
    def test_parse_html(self):
        self.fail()

    def test_find_product_list(self):
        self.fail()

    def test_zip(self):
        integers = [1, 2, 3]
        letters = ['a', 'b', 'c']
        floats = [4.0, 8.0, 10.0]
        zipped = zip(integers, letters, floats)
        list_data = list(zipped)
        print('list_data:{}'.format(list_data))
