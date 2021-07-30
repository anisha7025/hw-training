headers = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}


from lxml import html
import requests
import logging


logging.basicConfig(filename="walmart.log", filemode="w", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
logger = logging.getLogger()
url = 'https://www.walmart.com/ip/Apple-Watch-Series-3-GPS-38mm-Sport-Band-Aluminum-Case/706203065'
page = requests.get(url, headers=headers)
logging.info("requested the url...")
response = html.fromstring(page.content)
logging.info("got the response :)")


logger.info("started extraction")


specifications = {}
try:
	# XPATH
	BRAND_XPATH = '//a[@class="prod-brandName"]/span/text()'
	NAME_XPATH = '//h1[@class="prod-ProductTitle prod-productTitle-buyBox font-bold"]/text()'
	PRICE_XPATH = '//span[@class="price-characteristic"]/@content'
	OLD_PRICE_XPATH = '//span[@class="price display-inline-block xxs-margin-left price--strikethrough"]/span/text()'
	MODEL_XPATH = '//div[@class="valign-middle secondary-info-margin-right copy-mini display-inline-block other-info"]//text()'
	ITEM_XPATH = '//div[@class="valign-middle secondary-info-margin-right copy-mini display-inline-block wm-item-number"]//text()'
	DELIVERY_XPATH = '//div[@class="fulfillment-shipping-text"]/p/text()'
	DESCRIPTION_XPATH = '//div[@class="about-desc about-product-description xs-margin-top"]//text()'
	ROWS_XPATH = '//h3[text()="Specifications"]/following-sibling::table//tr'
	RATING_XPATH = '//span[@class="ReviewsRating-rounded-overall"]/span/text()'
	TOTAL_RATING_XPATH = '//div[@class="ReviewRatings-wrapper"]//div[@aria-hidden="true"]/text()'
	PERCENT_XPATH = '//div[@class="ReviewRecommend-container"]//span/text()'


	# EXTRACT
	brand_name = response.xpath(BRAND_XPATH)
	product_name = response.xpath(NAME_XPATH)
	price = response.xpath(PRICE_XPATH)
	old_price = response.xpath(OLD_PRICE_XPATH)
	model_no = response.xpath(MODEL_XPATH)
	item_no = response.xpath(ITEM_XPATH)
	delivery = response.xpath(DELIVERY_XPATH)
	description = response.xpath(DESCRIPTION_XPATH)
	rating_out_of_5 = response.xpath(RATING_XPATH)
	ratings = response.xpath(TOTAL_RATING_XPATH)
	rating_percent = response.xpath(PERCENT_XPATH)
	rows = response.xpath(ROWS_XPATH)



	# CLEAN
	brand_name = ''.join(brand_name) if brand_name else ''
	product_name = ''.join(product_name) if product_name else ''
	price = ''.join(price)
	old_price = ''.join(old_price)
	model_no = ''.join(model_no)
	item_no = ''.join(item_no)
	delivery = ''.join(delivery) 
	description = ''.join(description)
	rating_out_of_5 = ''.join(rating_out_of_5) 
	ratings = ''.join(ratings) 
	rating_percent =''.join(rating_percent) 
	for row in rows:
		key = row.xpath('td[1]/text()')[0]
		value = row.xpath('td[2]/div/text()')[0]
		specifications.update({key:value})


	logger.info('extracted')


	item = {}
	item['brand'] = brand_name
	item['name'] = product_name
	item['new_price'] = price
	item['old_price'] = old_price
	item['model_no'] = model_no
	item['item_no'] = item_no
	item['delivery'] = delivery
	item['description'] = description
	item['specifications'] = specifications
	item['rating_out_of_5'] = rating_out_of_5
	item['ratings'] = ratings
	item['rating_percent'] = rating_percent

	
	print(item)
	logger.info("printing...")

except Exception as e:
	print(e)
	logger.error("invalid xpath")

logger.info("exits the prgrm")
