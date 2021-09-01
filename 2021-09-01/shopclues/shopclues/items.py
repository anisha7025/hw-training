# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopcluesUrlItem(scrapy.Item):
    # define the fields for your item here like:
    __id = scrapy.Field()
    product_url = scrapy.Field()
    
class ShipcluesItem(scrapy.Item):
    __id = scrapy.Field()
    product_id = scrapy.Field()
    source  = scrapy.Field()
    scraped_date = scrapy.Field()
    product_name = scrapy.Field()   
    image_url = scrapy.Field() 
    category_hierarchy = scrapy.Field() 
    product_price = scrapy.Field()
    arrival_date = scrapy.Field()    
    shipping_charges = scrapy.Field()    
    is_sold_out = scrapy.Field() 
    discount = scrapy.Field()   
    mrp = scrapy.Field()
    product_url = scrapy.Field()
    number_of_ratings = scrapy.Field()  
    avg_rating = scrapy.Field()
    position = scrapy.Field()   
    country_code = scrapy.Field()
