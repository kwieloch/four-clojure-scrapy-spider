# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FourClojureItem(scrapy.Item):
    number = scrapy.Field()
    title = scrapy.Field()
    difficulty = scrapy.Field()
    cases = scrapy.Field()
    solution = scrapy.Field()
