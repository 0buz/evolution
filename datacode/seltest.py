import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time

headers={'User-agent' : 'Mozilla/5.0'}


Product=[]
Price=[]
Discount=[]

driver = webdriver.Chrome()

# for u in range(0,6):
#
#     url='https://www.delhaize.be/nl-be/shop/Dranken-en-alcohol/c/v2DRI?q=:relevance:manufacturerNameFacet:Coca-Cola:manufacturerNameFacet:Schweppes:manufacturerNameFacet:Fanta:manufacturerNameFacet:Chaudfontaine&sort=relevance&pageNumber=' + str(u)
#     driver.get(url)
#
#     try:
#         # makes the scraper wait until the element is loaded on the website
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'data-item')))
#
#         for products in driver.find_elements_by_xpath("//div[@class='description anchor--no-style']"):
#             Product.append(products.text.strip('\n'))
#
#         for prices in driver.find_elements_by_xpath("//span[@class='quantity-price super-bold']"):
#             Price.append(prices.text)
#             print(prices.text)
#
#         for promotions in driver.find_elements_by_xpath("//div[@class='PromotionStickerWrapper']"):
#             Discount.append(promotions)
#             print(promotions.text)
#
#         print('Scraping...')
#
#     except (NoSuchElementException, TimeoutException):
#         pass
#
# print(Product, Price, Discount)
# print(len(Product))
# print(len(Price))
# print(len(Discount))

for u in range(0,6):
    url='https://www.delhaize.be/nl-be/shop/Dranken-en-alcohol/c/v2DRI?q=:relevance:manufacturerNameFacet:Coca-Cola:manufacturerNameFacet:Schweppes:manufacturerNameFacet:Fanta:manufacturerNameFacet:Chaudfontaine&sort=relevance&pageNumber=' + str(u)
    driver.get(url)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'data-item')))

    for product in driver.find_elements_by_class_name("data-item"):
        # get the product list item by class name
        product_name = product.find_element_by_class_name("ProductHeader").text.replace("\n", " - ")
        # try to get the price span by class name with the product list item html else set it to zero
        try:
            product_price = product.find_element_by_class_name("quantity-price").text
            # clean the price by replace € and , and convert it to float
            float_product_price = float(product.find_element_by_class_name("quantity-price").text.replace("€","").replace(",","."))
        except NoSuchElementException:
            product_price = "0"
            float_product_price = 0
        # try to get the discount span by class name with the product list item html else set it to zero
        try:
            product_discount = product.find_element_by_class_name("multiLinePromotion").text
            # clean the discount by replace -  %  € and , and convert it to float
            float_product_discount = float (product.find_element_by_class_name("multiLinePromotion").text.replace("- ","").replace("%","").replace("€","").replace(",","."))
        except NoSuchElementException:
            product_discount ="0"
            float_product_discount = 0

        Product.append(product_name)
        Price.append(float_product_price)
        Discount.append(float_product_discount)



print(list(zip(Product, Price, Discount)))
print(len(Product))
print(len(Price))
print(len(Discount))