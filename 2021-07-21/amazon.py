from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from lxml import html

class Amazon_test:

  def __init__(self):
    self.driver = webdriver.Chrome()

    self.set_up()

  def set_up(self):  
    self.driver.maximize_window()
    time.sleep(2)

    self.driver.get("http://www.amazon.in")
    searchbox = self.driver.find_element_by_xpath('//input[@type="text"]')
    searchbox.send_keys('Mobiles')

    try:
      searchButton = self.driver.find_element_by_xpath('//input[@id="nav-search-submit-button"]')
      searchButton.click()
    except NoSuchElementException:
      print("Element does not exist")

    drop = self.driver.find_element_by_xpath("//a[@aria-label='See more, Brand']")
    drop.click()

    try:
      Apple = self.driver.find_element_by_xpath('//li[@aria-label="Apple"]/span/a') 
      Apple.click()
    except NoSuchElementException:
      print("Element does not exist")

    time.sleep(1)

    sort_by = Select(self.driver.find_element_by_xpath("//select[@class='a-native-dropdown a-declarative']"))
    sort_by.select_by_visible_text("Price: Low to High")

    time.sleep(10)

    self.parse_page()
  
  def parse_page(self):
    item = {}
    response = html.fromstring(self.driver.page_source)
    for info in response.xpath('//div[contains(@data-component-type ,"s-search-result")]'):
      product_name = info.xpath('div//span[@class="a-size-medium a-color-base a-text-normal"]/text()')[0]
      product_price = info.xpath('div//span[@class="a-offscreen"]/text()')[0]

      item["product_name"] = product_name
      item["product_price"] = product_price
  
      print(item)

    try:
      next_link = self.driver.find_element_by_xpath('//li[@class="a-last"]/a') 
      next_link.click()
      time.sleep(5)
      self.parse_page()
    except NoSuchElementException:
      self.driver.close()


run = Amazon_test()








