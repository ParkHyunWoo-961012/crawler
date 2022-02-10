# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AllnewscrawlerItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    time = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
