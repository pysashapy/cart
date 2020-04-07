import requests
import csv
import xlwt
from bs4 import BeautifulSoup
import json
class Pr(object):
    """docstring for property."""
    def __init__(self):
        self.run()
    def getJson(self):
        a = open("input.json","r",encoding="utf-8")
        a = a.read()
        json_string = json.loads(a)
        print(json_string["items"][0])
        url = "http://www.absolut-tds.com/catalog/gsmrepit/%s/"
        a = {i["id"]:{"url":url%i["id"],"name":i["name"],"id":i["id"],"price":i["price"],"available":i["available"]} for i in json_string["items"]}
        return a
    def search_get(self,out):
        a = {}
        for row in out:
            try:
                a[row["Артикул"].split("-")[-1]] =["http://opt-list.ru/admin/store_goods_edit/{0}/all_goods".format(row["Идентификатор товара в магазине"]),row["Цена продажи, без учёта скидок"],row["Остаток"],row["Артикул"]]
            except Exception as e:
                print(e)
        return a
    def run(self):

        self.__PRODUCT__ = self.getJson()

        out = csv.DictReader(open("input.csv","r"), delimiter=';')
        get_opt_list = self.search_get(out)
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Python Sheet 1")
        z = 0
        print(len(self.__PRODUCT__),list(self.__PRODUCT__.keys()))
        for i in self.__PRODUCT__.keys():
            sheet1.write(z, 0, z)
            sheet1.write(z, 1,  self.__PRODUCT__[i]["url"])
            sheet1.write(z, 2, self.__PRODUCT__[i]["name"])
            sheet1.write(z, 3, self.__PRODUCT__[i]["id"])
            sheet1.write(z, 4, self.__PRODUCT__[i]["price"])
            sheet1.write(z, 5,  self.__PRODUCT__[i]["available"])
            try:
                if get_opt_list[i]:
                    sheet1.write(z,6, "")
                    sheet1.write(z,7, get_opt_list[i][0])
                    sheet1.write(z,8, get_opt_list[i][1])
                    sheet1.write(z,9, get_opt_list[i][2])
                    sheet1.write(z,10,get_opt_list[i][3])
            except Exception as e:
                pass
            z+=1
        book.save("print.xls")

if __name__ == '__main__':

    a = Pr()
