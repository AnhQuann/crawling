from docx import Document
from crawler import linksStructure
from createFileWord import createFileWord, saveFileWord
import json

data = {}

with open('data.json') as dataJSON:
  data = json.load(dataJSON)

rootUrl = "http://baotanglichsu.vn"

for menuItems in data:
  for dropItemMenu in menuItems["Dropdown"]:
    if len(dropItemMenu["SubDropdownLv1"]) > 0:
      for dropItemLv1 in dropItemMenu["SubDropdownLv1"]:
        if len(dropItemLv1["SubDropdownLv2"]) > 0:
          for dropItemLv2 in dropItemLv1["SubDropdownLv2"]:
            createFileWord(
              rootUrl,
              dropItemLv2["Link"],
              'Home > {0} > {1} > {2} > {3}'.format(menuItems["Title"], dropItemMenu["Title"], dropItemLv1["Title"], dropItemLv2["Title"])
            )
        else:
          createFileWord(
            rootUrl,
            dropItemLv1["Link"],
            'Home > {0} > {1} > {2}'.format(menuItems["Title"], dropItemMenu["Title"], dropItemLv1["Title"])
          )
    else:
      createFileWord(
        rootUrl,
        dropItemMenu["Link"],
        'Home > {0} > {1}'.format(menuItems["Title"], dropItemMenu["Title"])
      )

saveFileWord("baotang.docx")