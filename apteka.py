import pandas as pd
from settings import APTEKA
from settings import TOKEN
import numpy as np
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class HomeBot:
    def __init__(self, drugs):
        self.drugs = drugs
        self.store = APTEKA.keys()
        self.prices_lst = []
        for d in self.drugs:
            chrome_options = Options()
            chrome_options.add_argument("user-data-dir=selenium")
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='driver\chromedriver')
            for k, v in APTEKA.items():
                result = v[1](url=v[0], driver=driver, drugs=d, apteka=k)
                self.prices_lst += result
            driver.close()
        df = pd.DataFrame(self.prices_lst, columns=['name', 'price', 'drugs', 'apteka', 'href'])
        df['price'].replace('', np.nan, inplace=True)
        df.dropna(subset=['price'], inplace=True)
        df.astype({'price': 'int64'})
        self.prices_df = df

    def min_prices(self):
        min_price = self.prices_df.groupby('drugs')['price'].transform(min) == self.prices_df['price']
        return self.prices_df[min_price]

    @staticmethod
    def message_to_telegchat(chat_id, mess):
        requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={mess}')

    @staticmethod
    def message_to_telegchat_doc(chat_id, doc):
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={chat_id}', files=doc)

    def message_minprice(self, chat_id):
        for index, row in self.min_prices().iterrows():
            an = f'Название: {row["name"]}; Цена: {row["price"]}; Запрос: {row["drugs"]}, Аптека: {row["apteka"]},' \
                 f' /recount_{index}, /TOP3_{index}, /order_{index}'
            self.message_to_telegchat(chat_id=chat_id, mess=an)

    def message_pricelst(self, chat_id):
        self.prices_df.to_csv('price_list.csv')
        self.message_to_telegchat_doc(chat_id, {'document': open(f'price_list.csv', 'rb')})

    def change(self, index):
        self.prices_df = self.prices_df.drop([index])
        print(self.prices_df)

    def message_top3(self, chat_id, index):
        drug = self.prices_df.loc[index, 'drugs']
        df = self.prices_df.loc[self.prices_df['drugs'] == drug]
        for index, row in df.sort_values(by='price', ascending=False).tail(3).iterrows():
            an = f'Название: {row["name"]}; Цена: {row["price"]}; Запрос: {row["drugs"]}, Аптека: {row["apteka"]},' \
                 f' /recount_{index}, /order_{index}'
            self.message_to_telegchat(chat_id=chat_id, mess=an)

    def ordering(self, index):
        link = self.prices_df.loc[index, 'href']
        key = self.prices_df.loc[index, 'apteka']
        print(key)
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=selenium")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='driver\chromedriver')
        driver.implicitly_wait(10)
        driver.get(link)
        if key == 'eapteka':
            driver.find_element_by_xpath(APTEKA[key][2]).click()
        elif key == 'piluli':
            driver.find_element_by_link_text('Купить').click()
        else:
            driver.find_element_by_class_name(APTEKA[key][2]).click()
        driver.close()
