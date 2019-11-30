from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import cv2 as cv
import time
from PIL import Image

user = '13798286303'
password = 'firstone18'
pic_name = 'pic.png'

class crack_bilibili_login():

    def __init__(self):
        self.url = 'https://www.bilibili.com'
        self.browser = webdriver.Chrome()
        self.pic_name = pic_name
        self.pw = password
        self.username = user


    def call_ver(self,username,pw):
        self.browser.get(self.url)
        self.browser.find_element_by_class_name('face').click()
        self.browser.find_element_by_id('login-username').send_keys(self.username)
        self.browser.find_element_by_id('login-passwd').send_keys(self.pw)
        self.browser.find_element_by_class_name('btn-login').click()
        time.sleep(2)

    def shoot_ver(self):
        pic = self.browser.find_element_by_class_name('geetest_absolute')
        self.browser.save_screenshot(pic_name)
        left = pic.location['x']
        top = pic.location['y']
        right = pic.location['x'] + pic.size['width']
        bottom = pic.location['y'] + pic.size['height']
        im = Image.open(pic_name)
        im = im.crop((left,top,right,bottom))
        im.save(pic_name)

    def get_image_height(self,img):
        pic = cv.imread(img)
        info = pic.shape
        return info[0]

    def get_image_width(self,img):
        pic = cv.imread(img)
        info = pic.shape
        return info[1]

    def locate_origin(self,img):
        height = self.get_image_height(img)
        width = self.get_image_width(img)
        for i in range(height):
            count = 0
            gap = 0
            ans = []
            for j in range(width):
                if self.is_yellow(i,j,img):
                    count += 1
                    print(str(count)+ ' line:' + str(i) + ' column: '+ str(j))
                else:
                    count = 0
                """
                if gap == 8:
                    count = 0
                    gap = 0

                if count == 8:
                    gap = 0
                """
                if count == 36:
                    print('target line located')
                    return i

        return 404

    def locate_target(self,img,line):
        width = self.get_image_width(img)
        image = cv.imread(img)
        hsv = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        count = 0
        gap = 0
        for e in range(width):
            if hsv[line,e][2] <= 156:
                count += 1
            else:
                count = 0

            if count == 36:
                print('target column located: ' + str(e-count))
                return e-count

        return 404

    def get_track_length(self,img):
        origin = self.locate_origin(img)
        if origin == 404:
            print('An error occured when obtaining line')
            exit()
        target_column = self.locate_target(img,origin)
        if target_column == 404:
            print('An error occured when obtaining target column')
            exit()
        return target_column-7

    def is_yellow(self,a,b,img):
        image = cv.imread(img)
        hsv_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        if (hsv_image[a,b] >= [26,43,46]).all() and (hsv_image[a,b] <= [34,255,255]).all():
            print(hsv_image[a,b])
            return True
        else:
            return False

    def is_yellow_column(self,a,b,c,img):
        x = a
        while x <= b:
            if self.is_yellow(x,c,img) == False:
                return False
            x += 1
        return True

    def get_track(self,distance):
        track = []
        current = 0
        mid = distance * 4 / 5
        t = 0.1
        v = 0

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def locate_botton(self):
        return self.browser.find_element_by_class_name('geetest_slider_button')

    def drag_and_slide(self,button,track):
        ActionChains(self.browser).click_and_hold(button).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        (0.5)
        ActionChains(self.browser).release().perform()

    def does_element_exist(self,element):
        try:
            self.browser.find_element_by_class_name(element)
        except NoSuchElementException:
            return False
        else:
            return True

    def run(self):
        """
        self.shoot_ver()
        botton = self.locate_botton()
        """
        dis = self.get_track_length(pic_name)
        track = self.get_track(dis)
        self.drag_and_slide(botton,track)
        time.sleep(4)
        if self.does_element_exist('geetest_refresh_1'):
            self.browser.find_element_by_class_name('geetest_refresh_1').click()
            time.sleep(3)
            self.run()
        else:
            time.sleep(5)
            self.browser.close()

if __name__ == '__main__':
    crack = crack_bilibili_login()
    crack.call_ver(user,password)
    crack.run()
