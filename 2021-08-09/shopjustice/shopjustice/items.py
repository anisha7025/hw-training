# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopjusticeUrlItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field()
    
class ShopjusticeItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    pdp_url = scrapy.Field()
    product_name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    breadcrumbs = scrapy.Field()
    variants = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()