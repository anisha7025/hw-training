# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from finishline.items import ShopjusticeUrlItem,ShopjusticeItem
from scrapy.exceptions import DropItem



class FinishlinePipeline:
    database = "shopjustice"
    collection1 = "product_data"
    collection2 = "product_links"


    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.db = self.client[self.database]
        self.coll1 = self.db[self.collection1]
        self.coll2 = self.db[self.collection2]
        self.coll2.create_index({"url":1},unique=True)

    def process_item(self, item, spider):
        if isinstance(item, ShopjusticeItem):
            try:
                self.coll1.insert_one(item)
            except Exception:
                raise DropItem("Dropping duplicate item")
        if isinstance(item, ShopjusticeUrlItem):
            try:
                self.coll2.insert_one(item)
            except Exception:
                raise DropItem("Dropping duplicate item")
        return item

    def close_spider(self,spider):
        self.client.close()