from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import OrderedDict
import time
import pyexcel


def crawlProfile(symbol):
  url = "http://en.stockbiz.vn/Stocks/{0}/Overview.aspx".format(symbol.strip())
  htmlContent = urlopen(url).read().decode("utf8")
  soup = BeautifulSoup(htmlContent, 'html.parser')
  main_table = soup.find_all('div', 'TableContent')[1]
  industry = main_table.find('table').find('tbody').findChildren("tr", recursive=False)[6].find('td', 'right').a
  address = main_table.find('table').find('tbody').findChildren("tr", recursive=False)[7].find('td', 'right').a
  return [industry.text if industry is not None else "---", address.text if address is not None else "---"]

data = []

driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://en.stockbiz.vn/CompanyAZ.aspx")
for i in range(89):
  print("Crawling symbols page {0}...".format(i+1))
  table = driver.find_element_by_id("ctl00_webPartManager_wp1961146353_wp44453090_gvResult").find_element_by_tag_name('tbody')
  rows = table.find_elements_by_tag_name('tr')
  del rows[0]
  for row in rows:
    company = OrderedDict({
      "Symbol": "",
      "Name": "",
      "Industry": "",
      "Address": ""
    })
    
    symbol = row.find_elements_by_tag_name('td')[1].text
    name = row.find_elements_by_tag_name('td')[2].text
    industry, address = crawlProfile(symbol)

    company['Symbol'] = symbol
    company['Name'] = name
    company['Industry'] = industry
    company['Address'] = address

    print(company)

    data.append(company)

  if i < 88:
    driver.execute_script("javascript:__doPostBack('ctl00$webPartManager$wp1961146353$wp44453090$lbtnNext','')")
    time.sleep(10)
  print("Done page {0}!".format(i+1))
  print("===============================================")
  pyexcel.save_as(records=data, dest_file_name="data.xlsx")

