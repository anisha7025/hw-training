from lxml import html
import requests

headers = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}

def parse_data(url):
    page=requests.get(url, headers=headers)
    response=html.fromstring(page.content)

    # XPATH
    NAME_XPATH='//h2[@class="product-title"]/text()'
    PRICE_XPATH='//span[@class="value"]/text()'
    COLOR_XPATH='//div[@class="color-swatch-wrapper--outer"]//a/span/@data-attr-value'
    SIZE_XPATH='//div[@data-attr="size"]/a/text()'
    IMAGE_XPATH = '//button[@class="product-main-image-thumbs-button"]/img/@data-yo-src'
    DESCRIPTION_XPATH='//div[@class="product-set-banner-details mb-3"]/text()'
    FEATURES_XPATH='//ul[@class="product-details-list"]/ul/li/text()'

    # EXTRACT
    product_name=response.xpath(NAME_XPATH)
    price = response.xpath(PRICE_XPATH)
    color=response.xpath(COLOR_XPATH)
    sizes=response.xpath(SIZE_XPATH)
    images=response.xpath(IMAGE_XPATH)
    description=response.xpath(DESCRIPTION_XPATH)
    features=response.xpath(FEATURES_XPATH)

    # CLEAN
    product_name =''.join(product_name) if product_name else ''
    price = ''.join(price).strip().replace('$','') if price else ''
    sizes = [size.strip() for size in sizes]
    images = [i.split('?')[0] for i in images]
    image_url = ', '.join(images)
    description = ''.join(description).strip()

    item = {}
    item['pdp_url']=url
    item['product_name']=product_name
    item['brand']="Carter's"
    item['price']=price
    item['currency']='USD'
    item['image_url']=image_url
    item['description']=description
    item['product_variants']={}
    item['product_variants']['color'] = color
    item['product_variants']['size'] = sizes
    item['features']=features
    try:
        print(item)
    except:
        pass
if __name__ == "__main__":
    # urls = []
    links = ['https://www.carters.com/carters-baby-girl-tops/V_1L732910.html', ]
    for url in links:
        parse_data(url)


