from classes import Product,Lazada
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys
import requests

def scrap_lazada(search_item,total_of_result):
    opts = Options()
    ua = UserAgent()
    userAgent = ua.random
    opts.add_argument(f'user-agenta={userAgent}')

    webdriver_path= "/usr/local/bin/chromedriver"
    Lazada_url = "https://www.lazada.sg"
    

    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('start-maximized') 
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')

    browser = webdriver.Chrome(webdriver_path,options=options)
    browser.get(Lazada_url)

    search_bar = browser.find_element_by_id("q")
    search_bar.send_keys(search_item)
    search_bar.submit()

    item_titles = browser.find_elements_by_class_name('c16H9d')
    item_prices = browser.find_elements_by_class_name('c13VH6')
    links = browser.find_elements_by_xpath("//div[@class='cRjKsc']/a")
    # pic_links = browser.find_elements_by_xpath("//div[@class='cRjKsc']/a/img")
    # pic_links = browser.find_elements_by_class_name('c1ZEkM')
    # print(len(pic_links))
    # for i in range(len(pic_links)):
    #     try:
    #         print(pic_links[i].get_attribute("src"))
    #     except IndexError:
    #         pass
    product_lst = []
    
    if len(item_titles)==0:
        print("Fail")
        sys.exit()

    
    for i in range(total_of_result):
        try:
            product_lst.append(Lazada(item_titles[i].text,item_prices[i].text,"",links[i].get_attribute("href"),""))
        except IndexError:
            pass
        
    
    for i in range(len(product_lst)):
        browser.get("{}".format(product_lst[i].url))
        ratings = browser.find_elements_by_class_name('score-average')
        ratings_count = browser.find_elements_by_class_name('count')
        num_of_ratings = [i for i in ratings_count[0].text if i.isdigit()==True]
        product_lst[i].ratings = ratings[0].text+"("+"".join(num_of_ratings)+")"
        pic_links = browser.find_elements_by_xpath("//div[@class='gallery-preview-panel__content']/img")
        product_lst[i].pic = pic_links[0].get_attribute('src')
        print(product_lst[i].pic)

    browser.quit()
    
    return product_lst

if __name__ == "__main__":
    df = pd.DataFrame([t.__dict__ for t in scrap_lazada("adidas shoes",5)])
    print(df)