#!/usr/bin/python3

import csv
import requests
import xlwt
from bs4 import BeautifulSoup
from time import *



class Test(object):
    """docstring for Test."""
    csv_path = "input.csv"
    __LIST__ = {}
    def __init__(self):
        super(Test, self).__init__()
        self.csv_reader(open(self.csv_path,"r"))
    def csv_reader(self,file_obj):
        a = {}
        out = csv.DictReader(file_obj, delimiter=';')
        ij = 0
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Python Sheet 1")
        for row in out:
            try:
                url = "http://www.absolut-tds.com/catalog/{0}/{1}/".format(*(row["Артикул"].split("-")))
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    price = soup.find_all("span", class_="woocommerce-Price-amount amount")[0].text
                    get = (soup.find_all("span", class_="sku_wrapper")[-1].text).split(":")[-1]
                    name = soup.find("h3", class_="product_title entry-title").text
                    print(url,"\n",price,get,name,ij)
                    try:
                        sheet1.write(ij, 0, ij+1)
                        sheet1.write(ij, 1, url)
                        sheet1.write(ij, 2, name)
                        sheet1.write(ij, 3, row["Артикул"])
                        sheet1.write(ij, 4, price)
                        sheet1.write(ij, 5, get)
                        sheet1.write(ij,6,"http://opt-list.ru/admin/store_goods_edit/{0}/all_goods".format(row["Идентификатор товара в магазине"]))
                    except Exception as e:
                        print("ошибка вставки в ячейку")
                    ij+=1
                except Exception as e:
                    print("ошибка полученой информации по url")

            except Exception as e:
                print("ошибка получение html сайта")

        book.save("print.xls")
if __name__ == "__main__":
    Test()
