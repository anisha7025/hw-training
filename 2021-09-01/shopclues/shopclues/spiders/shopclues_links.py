import scrapy
import re
from scrapy.http import Request
from ..items import ShopcluesUrlItem


headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent':' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Upgrade-Insecure-Requests': '1'
            }


class ShopcluesLinksSpider(scrapy.Spider):
    name = 'shopclues_links'
    allowed_domains = ['shopclues.com']
    base_url = 'https://www.shopclues.com/womens-clothing-ethnic-wear.html?scl=1&page='
    page_number = 2

    def start_requests(self):
        url = 'https://www.shopclues.com/womens-clothing-ethnic-wear.html?scl=1&page=1'
        yield Request(url, headers=headers)

    def parse(self, response):
        links = response.xpath('//div[@class="row"]/div/a[2]/@href').extract()
        for link in links:
            product_url = 'https:' + link


            item = ShopcluesUrlItem()
            item['product_url'] = product_url        

            yield item

        # next_page = response.url.split('page=')[0]+'page='+str(int(response.url.split('page=')[-1])+1)
        # if next_page:
        #     yield Request(next_page, headers=headers, callback=self.parse)


        total = response.xpath('//input[@id="prdCount"]/@value').extract_first()
        per_page_limit = response.xpath('//script[contains(text(),"userZoneCityPincode")]/text()').extract_first()
        limit = re.findall(r'product_perpage_limit = (\d+)',per_page_limit)[0]
        pages = int(int(total)/int(limit))
        if self.page_number <= pages :
            next_page = self.base_url + str(self.page_number)
            yield Request(next_page, headers=headers, callback=self.parse)
            self.page_number += 1