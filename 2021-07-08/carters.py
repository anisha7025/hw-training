headers = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}

from lxml import html
import requests
import re

url = 'https://www.carters.com/carters-baby-girl-tops/V_1L732910.html'
page=requests.get(url, headers=headers)
tree=html.fromstring(page.content)

product_name=tree.xpath('//h2[@class="product-title"]/text()')[0]
price = tree.xpath('//span[@class="value"]/text()')[0].strip()
match=re.match('(\$)(\d\.\d+)',price)
new_price=match.group(2)
brand=tree.xpath('//div[@class="logo"]/a/@title')[0]
# currency
# pdp_url=tree.xpath('')
color=tree.xpath('//div[@class="color-swatch-title"]/span/text()')
sizes=tree.xpath('//div[@data-attr="size"]/a/text()')
new_size=[size.strip() for size in sizes]
images=tree.xpath('//img[@class="js-product-main-image-0"]/@src')
desc=tree.xpath('//div[@class="product-set-banner-details mb-3"]/text()')
features=tree.xpath('//ul[@class="product-details-list"]//li/text()')[:3]



item={
    'product_name':product_name,
    'brand':brand,
    'price':new_price,
    'image_url':images,
    'desc':desc,
    'variants':{'color':color,
                'size':new_size
                },
    'features':features
}
print(item)