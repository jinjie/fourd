# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FourdItem(scrapy.Item):
    
    draw_date = scrapy.Field()
    draw_no = scrapy.Field()
    
    first = scrapy.Field()
    second = scrapy.Field()
    third = scrapy.Field()
    
    starters = scrapy.Field()
    
    consolations = scrapy.Field()
    
    pass
