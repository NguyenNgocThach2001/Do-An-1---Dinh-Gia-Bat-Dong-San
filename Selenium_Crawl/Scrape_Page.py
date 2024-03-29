from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

DSQH = {'Thành Phố Thủ Đức' :'https://batdongsan.com.vn/ban-nha-dat-thu-duc', 
        'Quận 1' :'https://batdongsan.com.vn/ban-nha-dat-quan-1', 
        'Quận 2' :'https://batdongsan.com.vn/ban-nha-dat-quan-2',
        'Quận 3' :'https://batdongsan.com.vn/ban-nha-dat-quan-3', 
        'Quận 4' :'https://batdongsan.com.vn/ban-nha-dat-quan-4', 
        'Quận 5' :'https://batdongsan.com.vn/ban-nha-dat-quan-5', 
        'Quận 6' :'https://batdongsan.com.vn/ban-nha-dat-quan-6', 
        'Quận 7' :'https://batdongsan.com.vn/ban-nha-dat-quan-7',
        'Quận 8' :'https://batdongsan.com.vn/ban-nha-dat-quan-8', 
        'Quận 9' :'https://batdongsan.com.vn/ban-nha-dat-quan-9', 
        'Quận 10' :'https://batdongsan.com.vn/ban-nha-dat-quan-10', 
        'Quận 11' :'https://batdongsan.com.vn/ban-nha-dat-quan-11', 
        'Quận 12' :'https://batdongsan.com.vn/ban-nha-dat-quan-12', 
        'Quận Bình Tân' :'https://batdongsan.com.vn/ban-nha-dat-binh-tan',
        'Quận Bình Thạnh' :'https://batdongsan.com.vn/ban-nha-dat-binh-thanh', 
        'Quận Gò Vấp' :'https://batdongsan.com.vn/ban-nha-dat-go-vap', 
        'Quận Phú Nhuận' :'https://batdongsan.com.vn/ban-nha-dat-phu-nhuan', 
        'Quận Tân Bình' :'https://batdongsan.com.vn/ban-nha-dat-tan-binh',
        'Quận Tân Phú' :'https://batdongsan.com.vn/ban-nha-dat-tan-phu', 
        'Huyện Bình Chánh' :'https://batdongsan.com.vn/ban-nha-dat-binh-chanh', 
        'Huyện Cần Giờ' :'https://batdongsan.com.vn/ban-nha-dat-can-gio', 
        'Huyện Củ Chi' :'https://batdongsan.com.vn/ban-nha-dat-cu-chi',
        'Huyện Hóc Môn' :'https://batdongsan.com.vn/ban-nha-dat-hoc-mon', 
        'Huyện Nhà Bè' :'https://batdongsan.com.vn/ban-nha-dat-nha-be'}

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

def Crawl_Page(City, num):
    print(DSQH.get(City))
    print(num / 20 + 1)
    News = Get_News_Links_FA2B(1, round(num / 20 + 1), DSQH.get(City))
    with open("page_data.txt", mode="w+") as txt_file:
        for it1 in News:
            for it2 in it1:
                txt_file.write(str(*it2) + "\n")