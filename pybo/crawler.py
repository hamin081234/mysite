import datetime

from bs4 import BeautifulSoup
import requests
import time
from datetime import date

class Crawler:

    def __init__(self):
        self.visited_list = []
        self.to_visit = []

    def parse_html(self, url):
        soup = None
        try:
            response = requests.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
            else:
                print('response.status_code:{}'.format(response.status_code))
                print("url을 확인 하세요")
        except Exception as e:
            print("*"*40)
            print("parse_html Exception: {}".format(e))
            print("*"*40)

        return soup

    def find_product_list(self, soup):
        if soup:
            pro_list = soup.select("div.pro_list>div>ul.proUl>li")
            product_id_list = []
            for product in pro_list:
                product_cd = product.get("data-product-cd")
                url = "https://www.iloom.com/product/detail.do?productCd="+product_cd
                product_detail = self.parse_html(url)
                self.product_info_parse(product_detail)

    def product_info_parse(self, product_detail):

        # 상품 상세 정보 박스 --------------------------------
        box_product_info = product_detail.select_one("div.box_productInfo")
        # 상품명
        product_name = box_product_info.select_one("div.productNm").text.strip()

        # 상품 가격
        product_price_txt = box_product_info.select_one("div.price").text.strip()[:-1]
        product_price = int(product_price_txt.replace(",", ""))

        # 상품 색깔 옵션
        select_color = box_product_info.select("select.select_color > option")
        colors = []
        for product in select_color:
            color = product.get("data-product-col")
            if color:
                colors.append(color)
        # 상품 상세 정보 박스 END --------------------------------

        # 상품 이미지 박스 -----------------------------
        box_product_gal = product_detail.select_one("ul.box_productGalery_S")
        img_src_list = box_product_gal.select("li>img")
        img_url_list = []
        for img_src in img_src_list:
            file_name = "a"
            img_url = img_src.get("src")
            if img_url:
                # img_url_list.append(img_url)
                f = open('C:/Users/hamin/Pictures/iloom/{}'.format(file_name), 'wb')
                f.write(requests.get(img_url).content)
                f.close()

        print()
        print("-"*40)
        print(product_name + " " + str(product_price) + " " + str(colors))
        # print(img_url_list)


def main():
    if __name__ == "__main__":
        crawler = Crawler()
        soup = crawler.parse_html("https://www.iloom.com/product/item.do?categoryNo=8")
        crawler.find_product_list(soup)


main()
