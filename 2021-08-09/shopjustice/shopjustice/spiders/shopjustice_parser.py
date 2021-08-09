import scrapy
from scrapy.http import Request
from ..items import ShopjusticeItem


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
        # urls = ['https://www.shopjustice.com/collections/all-products/products/2pc-short-set-jersey-top-with-sherpa-short-j168189-peach',
        #         'https://www.shopjustice.com/collections/all-products/products/taping-legging-452014-cat-dye-grey']
        # for url in urls:
        #     yield Request(url, callback=self.parse, headers=headers)

        file = open('shopjustice_links','r')
        Lines = file.readlines()
        count=0
        while(count <= 5):
            for url in Lines:
                # print(url)
                yield Request(url, callback=self.parse, headers=headers)
            count+=1
            # else:
            #     break

    def parse(self, response):
        # xpath
        name = response.xpath('//h1/text()').extract_first()
        brand = response.xpath('//span[@class="brand"]/text()').extract_first()
        price = response.xpath(
            '//div[@id="ProductPrice"]//span/text()').extract_first()
        breadcrumbs = response.xpath(
            '//nav[@aria-label="breadcrumbs"]//text()').extract()
        size = response.xpath('//span[@class="Size"]/text()').extract()
        color = response.xpath('//span[@class="Color"]/text()').extract_first()
        image = response.xpath(
            '//head/meta[@property="og:image"]/@content').extract_first()
        description = response.xpath(
            '//div[@id="ProductDescriptionBody"]//text()').extract()

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
