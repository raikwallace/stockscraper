# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockscrapyItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
