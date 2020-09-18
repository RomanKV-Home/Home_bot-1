from utils import apteka_ru
from utils import eapteka
from utils import zdravcity
from utils import zdesapteka
from utils import rigla
from utils import piluli


APTEKA = {
    'apteka_ru': [f'https://apteka.ru/search/?q=%s', apteka_ru, 'ProductPage__PurchaseButton'],
    'zdravcity': [f'https://zdravcity.ru/search/r_tula/?order=Y&what=%s', zdravcity, 'b-product-new__button'],
    'zdesapteka': [f'https://zdesapteka.ru/catalog/?q=%s', zdesapteka, 'to-cart '],
    'eapteka': [f'https://www.eapteka.ru/tula/search/?q=%s', eapteka, '//button[normalize-space()="Купить"]'],
    'rigla': [f'https://tula.rigla.ru/search?q=%s&city=Тула', rigla, 'product-cart__content-basket-btn'],
    'piluli': [f'https://tula.piluli.ru/search_result.html?q=%s', piluli, 'btn-wrap'],

}

TOKEN = "1053176976:AAGlYWWib1deLDPZqZ23uyJ7Q1enoWnWJvM" # token for test
