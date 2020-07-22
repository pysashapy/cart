import csv
import json
class Pr(object):
    """docstring for property."""
    def __init__(self):
        pass
    def getJson(self):
        a = open("input.json","r",encoding="utf-8")
        a = a.read()
        json_string = json.loads(a)
        print(json_string["items"][0])
        url = "http://www.absolut-tds.com/search/?q=%s"
        a = {i["barcode"]:{"url":url%i["barcode"],"name":i["name"],"id":i["id"],"barcode":i["barcode"],"price":i["price"],"real_q":i["real_q"]} for i in json_string["items"]}

        return a
    def wr(self,data=["JSON Остаток","JSON BarCode","JSON Цена","Название товара у орбиты","Ссылка от орбиты"],l=9):
        for i,x in zip(range(l,len(data)+l),data): self.row.insert(i, x)

    def run(self):
        self.__PRODUCT__ = self.getJson()
        with open('input.csv','r') as csvinput:
            with open('updata.csv', 'w',newline='') as csvoutput:
                new = csv.writer(csvoutput, delimiter=';')
                updata = csv.writer(open('new.csv', 'w',newline=''), delimiter=';')
                reader = csv.reader(csvinput, delimiter=';')

                newList = []
                updataList = []
                self.row = next(reader)
                self.wr()
                newList.append(self.row)

                reader1 = {i[4]:i for i in reader}
                for i in self.__PRODUCT__.keys():
                    a = self.__PRODUCT__[i]
                    try:
                        print(reader1.keys())
                        self.row = reader1[i]
                        self.wr([a["real_q"],i,a["price"],a["name"],a["url"]])
                        newList.append(self.row)
                    except Exception as e:
                        updataList.append([a["real_q"],i,a["price"],a["name"],a["url"]])

                new.writerows(newList)
                updata.writerows(updataList)
if __name__ == '__main__':

    a = Pr()
    a.run()
