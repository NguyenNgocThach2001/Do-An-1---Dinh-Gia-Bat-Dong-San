from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

def Create_Browser_Instance():
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--window-size=1920,1200")
    s = Service("C:\Program Files (x86)\Microsoft\Edge Webdriver\msedgedriver.exe")
    driver = webdriver.Edge(options= options, service = s)
    return driver

def Get_News_Links_With_Page(browser, source, pageNum):
    source = source + "/p" + str(pageNum)
    browser.get(source)
    News = []
    cnt = 1
    while(cnt != 21):
        value = "//div[@ipos='" + str(cnt) + "']"
        elem = browser.find_element(by=By.XPATH, value=value)
        if(elem != 0):
            a_elem = elem.find_element(by = By.CLASS_NAME, value='js__product-link-for-product-id')
            links = [a_elem.get_attribute('href')]
            News.append(links)
            cnt += 1
    return News

def Get_News_Links_FA2B(start, end, source):
    i = start
    News = []
    while(i != end + 1):
        print(i)
        browser = Create_Browser_Instance()
        News.append(Get_News_Links_With_Page(browser, source,i))
        browser.quit
        i += 1
    return News

def Filter():
    return 0

News = Get_News_Links_FA2B(1, 85, "https://batdongsan.com.vn/nha-dat-ban-quan-1")
with open("header_file.txt", mode="w+") as txt_file:
    for it1 in News:
        for it2 in it1:
            txt_file.write(str(*it2) + "\n")
