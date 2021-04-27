#!/usr/bin/python

import sys
import time
import random
# from win10toast import ToastNotifier
from selenium import webdriver
from settings import URLS


def get_stock(graphic_card_number, send, context):
    my_url = URLS.get(int(graphic_card_number))
    driver = webdriver.Firefox()

    while True:
        time.sleep(random.randint(3,8+1))
        driver.get(my_url)
        time.sleep(2)
        element = driver.find_element_by_class_name('buy')
        if element.text != 'AGOTADO':
            send(graphic_card_number, "🎉🎉🎉🎉🎉 STOCK!!! 🎉🎉🎉🎉🎉 \n HAY STOCK DE "+ str(graphic_card_number) + "!", context)


