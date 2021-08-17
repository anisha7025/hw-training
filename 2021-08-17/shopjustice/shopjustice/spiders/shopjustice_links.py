import scrapy
import json
from scrapy.http import Request
from ..items import ShopjusticeUrlItem


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept - encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.101 Safari/537.36 '

}


class ShopjusticeLinksSpider(scrapy.Spider):
    name = 'shopjustice_links'
    # allowed_domains = ['www.shopjustice.com']
    base_urls = 'https://www.shopjustice.com/collections/all-products/'

    def start_requests(self):
        urls = ['https://www.shopjustice.com/']
        for url in urls:
            yield Request(url, callback=self.parse, headers=headers)

    def parse(self, response):
        urls='https://toolbox.nogin.com/api/v1/products?publicToken=cko90ulz30000pzjsdzpbhyw0&s=&baseCollection=all-products&pageIndex=1&sortBy=manual&pageSize=36&faceted=true&facetedTagSet[]=type:&facetedTagSet[]=style:&facetedTagSet[]=\
        fit:&facetedTagSet[]=base_color:&facetedTagSet[]=sports_&outOfStock=false&exclude=imageId,sku,requiresShipping,bodyHtml,createdAt,publishedAt,productType,status,updatedAt,updateAt,document,sourceProductId,sourceImageId,inventoryPolicy,\
        taxable,grams,weight,weightUnit,inventoryItemId,inventoryQuantity,oldInventoryQuantity'
        yield Request(urls, headers=headers, callback=self.parse_link)
        
    def parse_link(self,response):
        # print(response.body)
        res = json.loads(response.body)
        items = res['items']
        for item in items:
            link = item['handle']
            new_url = self.base_urls + 'products/' + link


            item = ShopjusticeUrlItem()
            item['url'] = new_url

            yield item

            # with open('shopjustice_links', 'a') as outfile:
            #     outfile.write(new_url)
            #     outfile.write("\n")

            new_page = response.url.split('&pageIndex=')[0] + '&pageIndex=' + str(int(response.url.split('&pageIndex=')[1].split('&')[0])+1) + '&sort'+ response.url.split('&sort')[-1]
            if new_page :
                yield Request(new_page, headers=headers, callback=self.parse_link)