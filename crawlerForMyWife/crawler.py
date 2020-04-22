from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

url = "http://baotanglichsu.vn/en"
htmlContent = urlopen(url).read().decode("utf8")

soup = BeautifulSoup(htmlContent, 'html.parser')
menu = soup.find("ul", "navbar-nav")
menuItems = menu.findChildren("li", "dropdown", recursive=False)

exceptOptions = ["Museum Shop", "Organization"]

linksStructure = []

for menuItem in menuItems:
  menuItemStructure = {
    "Title": "",
    "Dropdown": [],
  }
  menuItemStructure["Title"] = menuItem.a.text
  dropdownItemsLv1 = menuItem.ul.findChildren("li", recursive=False)
  for dropdownItemLv1 in dropdownItemsLv1:
    dropdownItemLv1Structure = {
      "Title": "",
      "Link": "",
      "SubDropdownLv1": []
    }
    dropdownItemLv1Structure["Title"] = dropdownItemLv1.a.text
    if (dropdownItemLv1.has_attr("class")):
      dropdownItemsLv2 = dropdownItemLv1.ul.findChildren("li", recursive=False)
      for dropdownItemLv2 in dropdownItemsLv2:
        dropdownItemLv2Structure = {
          "Title": "",
          "Link": "",
          "SubDropdownLv2": []
        }
        dropdownItemLv2Structure["Title"] = dropdownItemLv2.a.text
        if (dropdownItemLv2.has_attr("class")):
          dropdownItemsLv3 = dropdownItemLv2.ul.findChildren("li", recursive=False)
          for dropdownItemLv3 in dropdownItemsLv3:
            dropdownItemLv3Structure = {
              "Title": dropdownItemLv3.a.text,
              "Link": dropdownItemLv3.a["href"]
            }
            dropdownItemLv2Structure["SubDropdownLv2"].append(dropdownItemLv3Structure)
        else:
          dropdownItemLv2Structure["Link"] = dropdownItemLv2.a["href"]
        dropdownItemLv1Structure["SubDropdownLv1"].append(dropdownItemLv2Structure)
    else:
      dropdownItemLv1Structure["Link"] = dropdownItemLv1.a["href"]
    if (dropdownItemLv1Structure["Title"] not in exceptOptions):
      menuItemStructure["Dropdown"].append(dropdownItemLv1Structure)
  linksStructure.append(menuItemStructure)

with open('data.json', 'w') as f:
  json.dump(linksStructure, f)