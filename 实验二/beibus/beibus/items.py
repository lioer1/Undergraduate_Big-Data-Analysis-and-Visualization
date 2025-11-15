# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeibusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    line_name = scrapy.Field()
    line_type = scrapy.Field()
    run_time = scrapy.Field()
    mileage = scrapy.Field()
    ticket = scrapy.Field()
    company = scrapy.Field()
    update_last = scrapy.Field()
    wang_info = scrapy.Field()
    fan_info = scrapy.Field()

