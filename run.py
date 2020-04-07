import requests
import csv
import xlwt
from bs4 import BeautifulSoup

class Pr(object):
    """docstring for property."""
    print(4)
    __URL__ = "http://www.absolut-tds.com"
    print(5)
    __URL_END_ = "http://www.absolut-tds.com/catalog/{0}/index.php?pp=99999&SECTION_CODE={0}"
    print(6)
    __URLs_CAT_ = []
    print(7)
    __PRODUCT__ ={}
    print(9)
    def __init__(self):
        print(3)
        self.getMenu()
    def int_str(self,i):
        print(13)
        try:
            int(i)
            return True
        except Exception as e:
            return False
    def soup_(self,url):
        print(14)
        html = requests.get(url).text
        return BeautifulSoup(html, 'html.parser')
    def urls_div(self,soup):
        print(15)
        return soup.find_all("div", id="content")
    def urls_a(self,soup,tg="a",class_=False,href=True):
        print((tg,class_,True))
        return soup.find_all(tg,class_=class_,href=href)
    def urls_end(self,soup):
        try:
            return soup.find_all("a",class_="page-numbers", href=True)[-1]["href"]
        except Exception as e:
            return None
    def search_get(self,out):
        a = {}
        for row in out:
            try:
                a[row["Артикул"].split("-")[-1]] =["http://opt-list.ru/admin/store_goods_edit/{0}/all_goods".format(row["Идентификатор товара в магазине"]),row["Цена продажи, без учёта скидок"],row["Остаток"],row["Артикул"]]
            except Exception as e:
                print(e)
        return a
    def getMenu(self):
        print(1)
        soup = self.soup_(self.__URL__+"/catalog/")
        for j in self.urls_a(soup,"a", class_="category"):
            self.__URLs_CAT_.append(self.__URL_END_.format(j["href"].split("/catalog/")[1][:-1]))
        print(self.__URLs_CAT_)
        self.run()
    def run(self):
        z1 = 0
        z2 = 999999999
        for url in self.__URLs_CAT_:
            for i in self.urls_a(self.soup_(url),"a",class_="woocommerce-LoopProduct-link"):
                a = self.soup_(self.__URL__+i["href"])
                if z1==z2:break
                try:
                    z = i["href"].split("/catalog/")[-1][:-1].split("/")
                    name = self.urls_a(a,tg="h3",class_="product_title entry-title",href=False)[-1].text
                    warehouse = self.urls_a(a,tg="span",class_="sku",href=False)[-1].text
                    price = self.urls_a(a,tg="span",class_="woocommerce-Price-amount amount",href=False)[-1].text
                    self.__PRODUCT__[z[-1]] = [name,self.__URL__+i["href"],"-".join(z),warehouse,price]
                    z1+=1
                except Exception as e:
                    raise
            if z1==z2:break
        out = csv.DictReader(open("input.csv","r"), delimiter=';')
        get_opt_list = self.search_get(out)
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Python Sheet 1")
        z = 0
        print(len(self.__PRODUCT__),list(self.__PRODUCT__.keys()))
        for i in self.__PRODUCT__.keys():
            sheet1.write(z, 0, z)
            sheet1.write(z, 1,  self.__PRODUCT__[i][0])
            sheet1.write(z, 2, self.__PRODUCT__[i][1])
            sheet1.write(z, 3, self.__PRODUCT__[i][2])
            sheet1.write(z, 4, self.__PRODUCT__[i][4])
            sheet1.write(z, 5,  self.__PRODUCT__[i][3])
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
