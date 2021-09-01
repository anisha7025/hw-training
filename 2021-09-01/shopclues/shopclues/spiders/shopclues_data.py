import scrapy
from scrapy.http import Request
from datetime import datetime
from ..items import ShipcluesItem


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent':' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Upgrade-Insecure-Requests': '1'}


class ShopcluesDataSpider(scrapy.Spider):
    name = 'shopclues_data'
    allowed_domains = ['shopclues.com']

    def start_requests(self):
        urls = ['https://www.shopclues.com/dnveens-black-heavy-zari-work-party-wear-georgette-salwar-kameez-women-dress-material-with-inner-141096770.html',
            'https://www.shopclues.com/women-shoppees-stylish-synthetic-salwar-suit-dupatta-unstiched-dress-material-142346522.html',
            'https://www.shopclues.com/cotton-silk-embroiderd-work-saree-with-jequard-blouse-151231722.html',
            'https://www.shopclues.com/meia-womens-japan-crep-silk-saree-pure-with-blouse-piece-151050651.html',
            'https://www.shopclues.com/aiza-collection-pecock-black-botton-yellow-dori-design-kurti-combo-pack-of-four-151321280.html',
            'https://www.shopclues.com/orange-kurta-plazzzo-set-152619445.html?adz_page=plp&adz_pos=1&campaign_id=39167'
]
        for url in urls:
            yield Request(url, headers=headers)

    def parse(self, response):

        PRODUCT_ID_XPATH = '//span[@class="pID"]/text()'
        PRODUCT_NAME_XPATH = '//h1/text()'
        IMAGE_XPATH = '//img[@itemprop="image"]/@src'
        CATEGORY_XPATH = '//li[@itemprop="itemListElement"]/a/span/text()'
        PRICE_XPATH = '//span[@class="f_price"]/@content'
        PRODUCT_DISCOUNT_XPATH = '//span[@class="discount"]/@content'
        MRP_XPATH = '//span[@id="sec_list_price_"]/@content'
        NO_OF_RATING_XPATH = '//span[@class="rating_num"]/@content'
        AVG_RATING_XPATH = '//span[@itemprop="ratingValue"]/text()'
        AVAILABILITY_XPATH = '//link[@itemprop="availability"]/@content'

        product_id = response.xpath(PRODUCT_ID_XPATH).extract()
        product_url = response.url
        product_name = response.xpath(PRODUCT_NAME_XPATH).extract_first()
        product_price = response.xpath(PRICE_XPATH).extract_first()
        category_hierarchy = response.xpath(CATEGORY_XPATH).extract()
        image_url = response.xpath(IMAGE_XPATH).extract_first()
        discount = response.xpath(PRODUCT_DISCOUNT_XPATH).extract_first()
        mrp = response.xpath(MRP_XPATH).extract_first()
        avg_rating = response.xpath(AVG_RATING_XPATH).extract_first()
        no_of_rating = response.xpath(NO_OF_RATING_XPATH).extract_first()
        availability = response.xpath(AVAILABILITY_XPATH).extract_first()
        if availability is not None:
            stock = availability.split('/')[-1] 
            if stock.lower() ==  "instock" :
                    is_sold_out = False
            else:
                    is_sold_out = True


        product_id = ''.join(product_id).strip()
        product_id = product_id.replace('Product Id :','')
        product_name = product_name.strip()
        category_hierarchy = '/'.join(category_hierarchy)


        item = ShipcluesItem()
        item['product_id'] = product_id  
        item['source'] = 'https://www.shopclues.com'  
        item['scraped_date'] = str(datetime.now().date())    
        item['product_name'] = product_name  
        item['image_url'] = image_url   
        item['category_hierarchy'] = category_hierarchy
        item['product_price'] = product_price  
        item['arrival_date'] = ''    
        item['shipping_charges'] = ''  
        item['is_sold_out'] = is_sold_out 
        item['discount'] = discount  
        item['mrp'] = mrp 
        item['product_url'] = product_url 
        item['number_of_ratings'] = no_of_rating  
        item['avg_rating'] = avg_rating 
        item['position'] = ''    
        item['country_code'] = 'IN'

        yield item