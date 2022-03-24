from cv2 import split
import requests
import csv
from bs4 import BeautifulSoup
from bs4 import NavigableString

url = "https://tinbatdongsan.com/nha-dat-ban.htm"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'
}

response = requests.post(url, headers=header)

print("Status code: ")
print(response.status_code)

body = BeautifulSoup(response.content, "lxml")
body_header_ul_li = body.find(id = "header").find("ul").findAll("li", recursive=False)

header_list = [];

def back_track(a, result):
    header_list.append(result)
    if(a.find("ul") is not None):
        a_ul = a.find("ul").findAll("li", recursive=False)
        for a_li in a_ul:
            sub_href = a_li.find("a", href=True)['href']
            if(a_li is not None):
                back_track(a_li, result + "," + sub_href)

cnt = 0
for a in body_header_ul_li:
    if(len(a.select("ul"))):
        header_href = a.find("a", href=True)['href']
        if(a is not None):
            back_track(a, header_href)

with open("header_file.txt", mode="w") as txt_file:
    for it in header_list:
        txt_file.write(it + "\n")



