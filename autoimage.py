from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

#Author: SunC-Mikasa

#Download images of certain title from image.baidu.com

#set photo amount you want to download
number = 50


url='https://image.baidu.com/'

search=input("你想要下载什么的图片？ >>")
driver=webdriver.Chrome()
driver.get(url)
searchs=search.replace('\"\"', '')
searchpic=driver.find_element_by_id("kw")
searchpic.send_keys(searchs)
icon= driver.find_element_by_class_name("s_search")
ActionChains(driver).click(icon).perform()
icons=driver.find_element_by_css_selector(".main_img.img-hover")
ActionChains(driver).click(icons).perform()


try_time=0
while try_time < number:
    driver.switch_to_window(driver.window_handles[1])
    if driver.find_element_by_class_name("btn-download"):
        element=driver.find_element_by_class_name("btn-download")
        ActionChains(driver).click(element).perform()
        driver.switch_to_window(driver.window_handles[1])
        elementss=driver.find_element_by_class_name("img-next")
        ActionChains(driver).click(elementss).perform()
        try_time+=1

    else:
        elementss=driver.find_element_by_class_name("img-next")
        ActionChains(driver).click(elementss).perform()

print(f"{try_time+1} pics downloaded.")
