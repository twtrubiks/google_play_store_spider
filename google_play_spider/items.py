# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglePlaySpiderItem(scrapy.Item):
     table_title = scrapy.Field()
     title = scrapy.Field()
     title_URL = scrapy.Field()
     imgURL = scrapy.Field()
     description = scrapy.Field()
     autor = scrapy.Field()
     autor_URL = scrapy.Field()
     star_rates = scrapy.Field()
     price  = scrapy.Field()

