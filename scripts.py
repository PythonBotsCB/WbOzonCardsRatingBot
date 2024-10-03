import requests
import json
import fake_useragent
from pprint import pprint

class WbCards():

    def __get(self, name:str) -> dict:
        ''' сборка айди товаров '''

        self.__url = 'https://catalog-ads.wildberries.ru/api/v6/search?keyword=' + name.replace(' ', '%20')
        self._headers = {
            'user-agent' : fake_useragent.UserAgent().random
        }

        # собираем айди товаров
        try:
            self.__all_cards = requests.get(self.__url, headers=self._headers).json()
        except Exception as ex:
            return {}

        return self.__all_cards

    def __collect(self, cards:dict) -> dict:
        ''' сборка всей информации о товаре '''

        self.__cards_info = {

        }

        for item in cards['adverts']:
            self.__url_item = f'https://card.wb.ru/cards/detail?appType=1&curr=rub&nm={item["id"]}'
            self.__card = requests.get(self.__url_item, headers=self._headers).json()

            self.__cards_info[item['id']] = {
                "name" : self.__card.get('data').get('products')[0].get('name'),
                "price" : f"{str(self.__card.get('data').get('products')[0].get('salePriceU'))[:-2]} ₽",
                "rate" : self.__card.get('data').get('products')[0].get('reviewRating'),
                "link" : f'https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
            }


        for id, info in self.__cards_info.items():
            if not(info.get('rate') > 4.4):
                self.__cards_info[id] = None

        return self.__cards_info

    def UploadInfo(self, request:str) -> dict:
        ''' Выгрузка всей информации '''

        self.__result = self.__collect(self.__get(request))

        self.__deleteNone()
        with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(self.__result, file, indent=4, ensure_ascii=False)

        return self.__result

    def __deleteNone(self):
        '''Избавляемся от None в словаре'''

        for id in list(self.__result.keys()):
            if self.__result[id] == None:
                del self.__result[id]

class OzonCards():

    def get(self):
        url = 'https://www.ozon.ru/category/usb-fleshki-15755/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D1%84%D0%BB%D0%B5%D1%88%D0%BA%D0%B0+64gb'
        headers = {
            'user-agent' : fake_useragent.UserAgent().random
        }

        html = requests.get(url, headers=headers).text

        with open('html.html', 'w') as file:
            file.write(html)

ozon = OzonCards()
ozon.get()