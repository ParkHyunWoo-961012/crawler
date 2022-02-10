# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import logging

import scrapy


class AllnewscrawlerItem(scrapy.Item):
    id = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    created_date = scrapy.Field()
    updated_date = scrapy.Field()

    def initialize(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value


