from time import sleep
from unittest import result
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import csv

def Create_Browser_Instance():
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--window-size=1920,1200")
    s = Service("C:\Program Files (x86)\Microsoft\Edge Webdriver\msedgedriver.exe")
    driver = webdriver.Edge(options= options, service = s)
    return driver

Page_List = []
with open("page_data.txt", "r", encoding="utf-8") as file:
    Page_List = file.readlines()

cnt = 0
tries = 0
with open("house_data.txt", "a", encoding="utf-8") as file:
    for it in Page_List:
        try: 
            tries += 1 
            print("tries: " + str(tries))
            browser = Create_Browser_Instance()
            browser.get(str(it))
            flag = False
            results = []
            while(flag == False):
                elem = browser.find_element(by = By.XPATH, value="/html/body/div[4]/div/div[1]/div[1]")
                if(elem != 0):
                    elem1 = browser.find_elements(by = By.XPATH, value="//*[@id='product-detail-web']/div[3]/div/div")
                    price = browser.find_element(by = By.XPATH, value="//*[@id='product-detail-web']/div[1]/div[1]/span[2]").get_attribute("innerText")
                    acreage = browser.find_element(by = By.XPATH, value="//*[@id='product-detail-web']/div[1]/div[2]/span[2]").get_attribute("innerText")
                    file.write("\n" + price + "\n" + acreage + "\n")
                    print(price)
                    print(acreage)
                    for it in elem1:
                        span_title = it.find_element(by = By.CLASS_NAME, value="title").get_attribute("innerText")
                        span_value = it.find_element(by = By.CLASS_NAME, value="value").get_attribute("innerText")
                        results.append(span_title + span_value + "\n")
                        print(span_title + span_value)
                    flag = True
            file.write("\n")
            for it in results:
                file.write(it)
            cnt += 1
            print("cnt: " + str(cnt))
            browser.quit
        except:
            browser.quit
            pass

print("Done")