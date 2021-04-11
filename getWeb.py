#!/usr/bin/python

import sys
import time
import random
from win10toast import ToastNotifier
from selenium import webdriver

urls = {
    3080: "https://shop.nvidia.com/es-es/geforce/store/gpu/?page=1&limit=9&locale=es-es&category=GPU&gpu=RTX%203080",
    3070: "https://shop.nvidia.com/es-es/geforce/store/gpu/?page=1&limit=9&locale=es-es&category=GPU&gpu=RTX%203070"
    }

my_url = urls.get(int(sys.argv[1]))
driver = webdriver.Firefox()
toaster = ToastNotifier()

while True:
    time.sleep(random.randint(3,8+1))
    driver.get(my_url)
    time.sleep(2)
    element = driver.find_element_by_class_name('buy')
    if element.text != 'AGOTADO':
        toaster.show_toast("🎉🎉🎉🎉🎉 STOCK!!! 🎉🎉🎉🎉🎉","HAY STOCK DE "+sys.argv[1]+'!')
    else:
        print("😢😢😢😢😢😢😢😢😢 NO HAY STOCK DE "+sys.argv[1]+'!')


