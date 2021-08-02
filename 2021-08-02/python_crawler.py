headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

from lxml import html
import requests


def parse_page(url):
    base_url = 'https://www.finishline.com'
    page = requests.get(url, headers=headers)
    response = html.fromstring(page.content)

    links = response.xpath('//div[@class="product-card__details"]//a[@class="hover-underline"]/@href')
    for link in links:
        urls = base_url + link
        print(urls)

    partial_url = response.xpath('//a[contains(@class,"pag-button next")]/@href')[0]
    new_url = base_url + partial_url
    print(new_url)
    try:
        parse_page(new_url)
    except:
        pass


url = 'https://www.finishline.com/store/men/shoes/casual/_/N-1q3xsyk?icid=LP_mgl_C_menslpcategorycasualshoes_PDCT'
run = parse_page(url)
