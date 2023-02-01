import datetime

from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import random
import csv


def csv_save(csv_path, row):
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


class Crawler:
    def __init__(self):
        # 크롤링을 시작 할 페이지
        self.start_url = "https://www.iloom.com/product/item.do?categoryNo=8&pageNo="
        self.visited_list = set()
        self.to_visit = set()
        # 상품과 연결될 카테고리
        self.category = ['침실', '침대']
        # csv 파일이 저장될 경로
        self.csv_path = "C:/Users/hamin/Desktop/crawling_data/"
        # 이미지 파일이 저장될 경로
        self.img_path = 'C:/Users/hamin/Pictures/iloom/'

    def parse_html(self, url):
        if url in self.visited_list:
            return

        soup = None
        try:
            response = requests.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                self.visited_list.add(url)
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
            product_cd_list = []
            for product in pro_list:
                product_cd = product.get("data-product-cd")
                product_cd_list.append(product_cd)
            return product_cd_list

    def product_info_parse(self, product_cd):
        url = "https://www.iloom.com/product/detail.do?productCd=" + product_cd
        product_detail = self.parse_html(url)

        # 상품 상세 정보 박스 --------------------------------
        box_product_info = product_detail.select_one("div.box_productInfo")
        # 상품명
        product_name = box_product_info.select_one("div.productNm").text.strip()

        # 상품 가격
        product_price_txt = box_product_info.select_one("div.price").text.strip()[:-1]
        # 판매가
        product_sp = int(product_price_txt.replace(",", ""))
        # 원가
        product_op = int((7/10*product_sp)/1000)*1000

        # product 테이블 데이터 추가 ---------------
        product_csv_path = self.csv_path+"product.csv"
        # [상품 코드, 상품명, 판매가, 원가, 진열 상태, 판매 상태, 상품 이미지 코드]
        row = [product_cd, product_name, product_sp, product_op, 1, 1, product_cd + "_img"]
        csv_save(product_csv_path, row)

        # 상품 카테고리 연결 ----------------
        conn_csv_path = self.csv_path+"connection.csv"
        for category in self.category:
            row = [product_cd, category]
            csv_save(conn_csv_path, row)

        # 상품 색깔 옵션 ---------------------
        select_color = box_product_info.select("select.select_color > option")
        for product in select_color:
            color = product.get("data-product-col")
            if color:
                opt_csv_path = self.csv_path+"option_product.csv"
                # [상품 아이디, 옵션 추가 플래그, 옵션 상품명, 상품 가격, 수향]
                row = [product_cd, 0, product_cd + "_" + str(color), product_sp, 100]
                csv_save(opt_csv_path, row)

        # 상품 상세 정보 박스 END --------------------------------

        # 상품 이미지 박스 -----------------------------
        box_product_gal = product_detail.select_one("ul.box_productGalery_S")
        img_src_list = box_product_gal.select("li>img")
        for img_src in img_src_list:
            file_num = str(random.randint(1,100000))
            while len(file_num) < 5:
                file_num = "0"+file_num
            img_url = img_src.get("src")
            if img_url:
                file_name = product_cd+"_"+file_num+"_"+str(round(time.time()))+".png"

                # 이미지 저장
                img_path = self.img_path + file_name
                with open(img_path, 'wb') as f:
                    f.write(requests.get(img_url).content)

                # 이미지와 상품 연결
                img_csv_path = self.csv_path + "image.csv"
                # [상품 코드, 이미지 종류, 이미지 파일명]
                row = [product_cd + "_img", 1, file_name]
                csv_save(img_csv_path, row)

    def find_url_to_visit(self, soup):
        # print(soup.select("div.list_cnt > ul.list_cnt_ul > li"))
        print(soup.select("div.list_cnt"))

    def investigate_page(self, url, page_no):
        # 페이지 정보 가져오기
        soup = self.parse_html(url+str(page_no))
        if not soup:
            return

        # 현재 페이지 속에 있는 상품 코드들
        product_cd_list = self.find_product_list(soup)
        if not product_cd_list:
            return
        # print(product_cd_list)

        # 코드들로 상품 상세 페이지로 가서 상세 정보 가져오기
        for product_cd in product_cd_list:
            self.product_info_parse(product_cd)

        # 현재 페이지에서 방문해야될 url 찾기
        self.investigate_page(url, page_no+1)

    def run(self):
        self.investigate_page(self.start_url, 1)


def main():
    if __name__ == "__main__":
        crawler = Crawler()
        crawler.run()


main()
