import requests
import csv
import xlwt
from bs4 import BeautifulSoup



def int_str(i):
    try:
        int(i)
        return True
    except Exception as e:
        return False

def soup_(url):
    html = requests.get(url).text
    return BeautifulSoup(html, 'html.parser')

def urls_div(soup):
    return soup.find_all("div", id="content")

def urls_a(soup,class_=False):
    return soup.find_all("a",class_=class_,href=True)
def urls_end(soup):
    try:
        return soup.find_all("a",class_="page-numbers", href=True)[-1]["href"]
    except Exception as e:
        return None
def search_get(out):
    a = {}
    for row in out:
        try:
            a[row["Артикул"].split("-")[-1]] =["http://opt-list.ru/admin/store_goods_edit/{0}/all_goods".format(row["Идентификатор товара в магазине"]),row["Цена продажи, без учёта скидок"],row["Остаток"],row["Артикул"]]
        except Exception as e:
            print(e)
    return a
def test():
    print("http://www.absolut-tds.com/catalog/gsmrepit/11823/".split("/")[-2])
def main():
    __URL__ = "http://www.absolut-tds.com/catalog/"
    __URL_END_ = "http://www.absolut-tds.com/catalog/{0}/index.php?pp=99999&SECTION_CODE={0}"
    __URLs_CAT_ = []
    __URL_PRODUCT__ = []
    __URL_PRODUCTS__ = {}
    soup = soup_(__URL__)
    for i in urls_div(soup):
        for j in urls_a(i):
            __URLs_CAT_.append(__URL_END_.format(j["href"].split("/catalog/")[1][:-1]))
    print(__URLs_CAT_)
    for ij in __URLs_CAT_:
        for i in urls_div(soup_(ij)):
            a = urls_a(i,class_=True)
            if a:
                for zij in a:
                    __URL_PRODUCT__.append(__URL__+(zij["href"].split("/catalog/")[1]))
            else:
                try:
                    for j in urls_a(i):
                        try:
                            for x in urls_div(soup_(__URL_END_.format(j["href"].split("/catalog/")[1][:-1]))):
                                a = urls_a(x,class_=True)
                                for zij in a:
                                    __URL_PRODUCT__.append(__URL__+(zij["href"].split("/catalog/")[1]))

                        except Exception as e:
                            pass
                except Exception as e:
                    raise
    z=1
    for i in __URL_PRODUCT__:
        try:
            soup = soup_(i)
            price = soup.find_all("span", class_="woocommerce-Price-amount amount")[0].text
            get = (soup.find_all("span", class_="sku_wrapper")[-1].text).split(":")[-1]
            name = soup.find("h3", class_="product_title entry-title").text
            __URL_PRODUCTS__[i.split("/")[-2]] = [i,name,price,get,i.split("/")[-2]+"-"+i.split("/")[-2]]
            print(__URL_PRODUCTS__[i.split("/")[-2]])
            z+=1
        except Exception as e:
            print("НЕ НАЙДЕНО")

    out = csv.DictReader(open("input.csv","r"), delimiter=';')
    get_opt_list = search_get(out)
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Python Sheet 1")
    z = 0
    for i in __URL_PRODUCTS__.keys():
        try:
            if get_opt_list[i]:
                sheet1.write(z, 0, z)
                sheet1.write(z, 1,  __URL_PRODUCTS__[i][0])
                sheet1.write(z, 2, __URL_PRODUCTS__[i][1])
                sheet1.write(z, 3, __URL_PRODUCTS__[i][2])
                sheet1.write(z, 4, __URL_PRODUCTS__[i][3])
                sheet1.write(z, 5,  __URL_PRODUCTS__[i][4])
                sheet1.write(z,6, "")
                sheet1.write(z,7, get_opt_list[i][0])
                sheet1.write(z,8, get_opt_list[i][1])
                sheet1.write(z,9, get_opt_list[i][2])
                sheet1.write(z,10,get_opt_list[i][3])
        except Exception as e:
            sheet1.write(z, 0, z)
            sheet1.write(z, 1,  __URL_PRODUCTS__[i][0])
            sheet1.write(z, 2, __URL_PRODUCTS__[i][1])
            sheet1.write(z, 3, __URL_PRODUCTS__[i][2])
            sheet1.write(z, 4, __URL_PRODUCTS__[i][3])
            sheet1.write(z, 5, i)

        z+=1
    book.save("print.xls")
if __name__ == '__main__':
    test1 = 0
    if test1:
        test()
    else: main()
