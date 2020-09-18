# from settings import APTEKA
def isint(price):
    try:
        int(price)
        price = int(price)
    except ValueError:
        price = int(10000000000)
    return price


def apteka_ru(url, driver, drugs, apteka):
    # driver.get(auth_url)
    # driver.get(auth_url)
    # driver.find_element_by_class_name('HeaderUserButton__login').click()
    # driver.find_element_by_class_name('auth-input').send_keys(log)
    # driver.find_element_by_class_name('auth__input-password').send_keys(pas)
    # driver.find_element_by_class_name('submit').click()
    url = url % drugs
    driver.implicitly_wait(10)
    driver.get(url)
    driver.get(url)
    # auth(driver, 'auth-input', 'auth__input-password', log, pas, 'HeaderUserButton__login')
    # driver.find_element_by_class_name('HeaderUserButton__login').click()
    # driver.find_element_by_class_name('auth-input').send_keys(log)
    # driver.find_element_by_class_name('auth__input-password').send_keys(pas)
    # driver.find_element_by_class_name('submit').click()
    total = []
    try:
        cards = driver.find_elements_by_class_name('CategoryItemCard')
        for card in cards:
            name = card.find_element_by_class_name('emphasis').text
            print(name)
            href = card.find_element_by_class_name('CategoryItemCard__title').get_attribute('href')
            print(href)
            price = card.find_element_by_class_name('CategoryItemCard__price').text
            print(price)
            # price = price.find_element_by_tag_name('strong').text
            price = price[price.find(':') + 1:price.find('.')].replace('от', '').strip()
            print(price)
            price = isint(price)
            print(price)
            new = ((name, price, drugs, apteka, href))
            total.append(new)
    except Exception:
        cards = driver.find_elements_by_class_name('ProductPage')
        for card in cards:
            name = card.find_element_by_class_name('ProductPage__title').text
            print(name)
            href = card.find_element_by_class_name('ProductPage__title').get_attribute('href')
            print(href)
            price = card.find_element_by_class_name('ProductPage__price').text
            print(price)
            # price = price.find_element_by_tag_name('strong').text
            price = price[0:price.find('.')]
            print(price)
            price = isint(price)
            print(price)
            new = ((name, price, drugs, apteka, href))
            total.append(new)


    # driver.close()
    return total


def zdravcity(url, driver, drugs, apteka):
    url = url % drugs
    driver.implicitly_wait(10)
    driver.get(url)
    driver.get(url)
    total = []
    cards = driver.find_elements_by_class_name('b-product-item-new--issue')
    for card in cards:
        name = card.find_element_by_class_name('b-product-item-new__group').text
        href = card.find_element_by_class_name('b-product-item-new__title').get_attribute('href')
        price = card.find_element_by_class_name('b-product-item-new__panel-middle').text
        # price = price.find_element_by_tag_name('span').text
        price = price[0:price.find('.')]
        price = price.replace('нет в наличи', '')
        price = isint(price)
        # print(price)
        new = ((name, price, drugs, apteka, href))

        total.append(new)
    # driver.close()
    return total


def zdesapteka(url, driver, drugs, apteka):
    url = url % drugs
    driver.implicitly_wait(10)
    driver.get(url)
    total = []
    cards = driver.find_elements_by_class_name('main_item_wrapper')
    # print(len(cards))
    for card in cards:
        name = card.find_element_by_class_name('item-title').text
        href = card.find_element_by_class_name('dark_link').get_attribute('href')
        price = card.find_element_by_class_name('price_value').text
        # price = price.find_element_by_tag_name('span').text
        # price = price[0:price.find('руб')]
        price = isint(price)
        new = ((name, price, drugs, apteka, href))

        total.append(new)
    # driver.close()
    return total


def eapteka(url, driver, drugs, apteka):
    url = url % drugs
    driver.implicitly_wait(10)
    driver.get(url)
    total = []
    cards = driver.find_elements_by_class_name('cc-item')
    for card in cards:
        name = card.find_element_by_class_name('cc-item--title').text
        price = card.find_element_by_class_name('price--new')
        href = card.find_element_by_class_name('cc-item--title').get_attribute('href')
        price = price.find_element_by_tag_name('span').text
        # price = price[0:price.find('i')]
        price = price.replace(' ', '')
        price = isint(price)
        # print(price)
        new = ((name, price, drugs, apteka, href))
        total.append(new)
    # driver.close()
    return total


def rigla(url, driver, drugs, apteka):
    url = url % drugs
    driver.implicitly_wait(10)
    driver.get(url)
    total = []
    cards = driver.find_elements_by_class_name('product')
    for card in cards:
        name = card.find_element_by_class_name('product-description').text
        price = card.find_element_by_class_name('product__active-price')
        href = card.find_element_by_class_name('product__title').get_attribute('href')
        price = price.find_element_by_tag_name('span').text
        # price = price[0:price.find('i')]
        price = isint(price)
        new = ((name, price, drugs, apteka, href))
        total.append(new)
    # driver.close()
    return total


def piluli(url, driver, drugs, apteka):
    url = url % drugs
    driver.implicitly_wait(10)
    driver.get(url)
    total = []
    cards = driver.find_elements_by_class_name('col-wrapper')
    for card in cards:
        name = card.find_element_by_class_name('details').text
        price = card.find_element_by_class_name('price-wrap').text
        href = card.find_element_by_class_name('title').get_attribute('href')
        # price = price.find_element_by_tag_name('span')
        # price = price.find_element_by_class_name('product_item_price_digit').text
        price = price.replace('Цена', '')
        price = price[0:price.find('руб')].strip()
        # price = price.replace('руб.', '').strip()
        price = isint(price)
        new = ((name, price, drugs, apteka, href))
        total.append(new)
    # driver.close()
    return total
