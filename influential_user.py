from bs4 import BeautifulSoup
import requests
import csv
with open("path to file","w",newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Rank","name","user_name"])
    f.close()
for i in range (#desired range):
    url = ""                    #url of the website. we used social bakers
    page = requests.get(url).text
    parsed = BeautifulSoup(page,'lxml')
    table = parsed.find("div",class_ = "brand-table-placeholder")
    for row in table.find_all("tr"):
        if row == table.find("tr",class_ = "replace-with-show-more"):
            break
        rank = row.find("i",class_ = "item-count").text
        name = row.find("h2").text.split("(")[0]
        user_name = row.find("h2").text.split("(")[1].replace(")","")
        with open("influential_user_list.csv","a",newline='') as f:
            writer = csv.writer(f)
            writer.writerow([rank,name.encode("utf-8"),user_name.encode("utf-8")])
            f.close()
print("completed")
