import scrapy
from scrapy.http import Request
from ..items import ShopjusticeItem
import pika
import logging


logger = logging.getLogger('pika')
logger.propagate = False


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
    '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept - encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/91.0.4472.101 Safari/537.36 '
}

variants = {}


class ShopjusticeParserSpider(scrapy.Spider):
    name = 'shopjustice_parser'
    allowed_domains = ['shopjustice.com']

    def start_requests(self):
        # from file
        # file = open('shopjustice_links','r')
        # Lines = file.readlines()
        # for url in Lines:
        #     # print(url)
        #     yield Request(url, callback=self.parse, headers=headers)

        # from queue
        count = 1
        credentials = pika.PlainCredentials('guest','guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters( host='localhost', socket_timeout=300))
        channel = connection.channel()
        while count <= 200:
            channel.basic_qos(prefetch_count=1)
            method, properties, url = channel.basic_get(queue='shopjustice')
            if not url.strip():
                break
            channel.basic_ack(delivery_tag=method.delivery_tag)
            url = str(url.strip(), encoding='utf-8')
            if url.strip():
                link = url
                yield Request(url=link.strip(), callback=self.parse, headers=headers)
                # print(url)
                count += 1
        connection.close()
           
    def parse(self, response):
        #xpath
        NAME_XPATH = '//h1/text()'
        BRAND_XPATH = '//span[@class="brand"]/text()'
        PRICE_XPATH = '//div[@id="ProductPrice"]//span/text()'
        BREADCRUMBS_XPATH = '//nav[@aria-label="breadcrumbs"]//text()'
        SIZE_XPATH = '//span[@class="Size"]/text()'
        COLOR_XPATH = '//span[@class="Color"]/text()'
        IMAGE_XPATH = '//head/meta[@property="og:image"]/@content'
        DESCRIPTION_XPATH = '//div[@id="ProductDescriptionBody"]//text()'
        
        name = response.xpath(NAME_XPATH).extract_first()
        brand = response.xpath(BRAND_XPATH).extract_first()
        price = response.xpath(PRICE_XPATH).extract_first()
        breadcrumbs = response.xpath(BREADCRUMBS_XPATH).extract()
        size = response.xpath(SIZE_XPATH).extract()
        color = response.xpath(COLOR_XPATH).extract_first()
        image = response.xpath(IMAGE_XPATH).extract_first()
        description = response.xpath(DESCRIPTION_XPATH).extract()

        # clean
        price = price.replace('$', '') if price else ''
        breadcrumbs = ''.join([i.strip() for i in breadcrumbs]) if breadcrumbs else ''
        description = ''.join([i.strip() for i in description]) if description else ''
        variants.update({'size':size})
        variants.update({'color':color})


        item = ShopjusticeItem()
        item['product_name'] = name
        item['brand'] = brand
        item['price'] = price
        item['currency'] = 'USD'
        item['breadcrumbs'] = breadcrumbs
        item['pdp_url'] = response.url
        item['variants'] = variants
        item['image_url'] = image
        item['description'] = description
    
        yield item

