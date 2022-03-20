import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

url = "https://batdongsanonline.vn/"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'
}

response = requests.post(url, headers=header)

print("Status code: ")
print(response.status_code)

body_header = BeautifulSoup(response.content, "html.parser")
body_header = body_header.find(id = "header")
print("Body_header")
print(str(body_header))

with open('Crawl.html','w', encoding="utf-8") as f:
    f.write(str(body_header))   


print("Child li")
for i in body_header.findChildren("li", recursive=False):
    print(i)

