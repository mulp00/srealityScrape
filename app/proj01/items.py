# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Proj01Item(scrapy.Item):
    description = scrapy.Field()
    image = scrapy.Field()
