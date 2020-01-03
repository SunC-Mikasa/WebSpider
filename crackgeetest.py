from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import random
import cv2 as cv
import time
from PIL import Image

#succeed in a time: 14
#fail to find & succeed in one retry: 3
#fail to find & succeed in more retries: 1
#find the wrong match & succeed in one retry: 1
#find the wrong match & succeed in more retries: 1
#detected: 1

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
        self.wait = WebDriverWait(self.browser, 5)

    def open_login_page(self):
        self.browser.get(self.url)
        face = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logout-face')))
        face.click()

    def call_ver(self,username,pw):
        all_h = self.browser.window_handles
        self.browser.switch_to.window(all_h[1])
        input_username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        input_username.send_keys(self.username)
        self.browser.find_element_by_id('login-passwd').send_keys(self.pw)
        self.browser.find_element_by_class_name('btn-login').click()
        time.sleep(2)
        print('OK，起飞')

    def shoot_ver(self):
        time.sleep(1.5)
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

    def locate_origin_line(self,img,start_line):
        position = []
        height = self.get_image_height(img)
        width = self.get_image_width(img)
        if start_line == height:
            return 404

        for i in range(start_line,height):
            count = 0
            gap = 0
            for j in range(round(width/3)):
                if self.is_yellow(i,j,img):
                    count += 1
                    print(str(count)+ ' 因为你不会 ' + str(i) + ' 所以你才会 '+ str(j))
                else:
                    gap += 1

                if count == 10:
                    gap = 0

                if gap == 5:
                    count = 0
                    gap = 0

                if count + gap == 36:  #36
                    print('你，只看到了第二层')
                    return i

        return 404

    def locate_origin_column(self,img,line):
        count = 0
        gap = 0
        width = self.get_image_width(img)
        for i in range(width):
            if self.is_yellow(line,i,img):
                count += 1
            else:
                gap += 1

            if count == 10:
                gap = 0

            if gap == 5:
                gap = 0
                count = 0

            if count + gap == 36:
                return i-count-gap

        return 404

    def locate_target(self,img,line):
        width = self.get_image_width(img)
        image = cv.imread(img)
        hsv = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        count = 0
        for e in range(width):
            if hsv[line,e][2] <= 156:
                count += 1
            else:
                count = 0

            if count == 36:
                time.sleep(2)
                print('而你把我，想成了第一层 ' + str(e-count))
                return e-count

        return 404

    def get_track_length(self,img):
        origin = self.locate_origin_line(img,1)
        if origin == 404:
            print('这波啊，这波是肉弹冲击')
            return 404
        target_column = self.locate_target(img,origin)
        while target_column == 404:
            origin = self.locate_origin_line(img,origin+1)
            if origin == 404:
                return 404
            target_column = self.locate_target(img,origin)
        return target_column-self.locate_origin_column(img,origin)

    def is_yellow(self,a,b,img):
        image = cv.imread(img)
        hsv_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
        if (hsv_image[a,b] >= [26,43,46]).all() and (hsv_image[a,b] <= [34,255,255]).all():
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
        '''
        current = 0
        change1 = distance * 1 / 5
        change2 = distance * 1 / 2
        change3 = distance * 5 / 6
        t = 0.1
        v = 0

        while current < distance:
            if current < change1:
                a = 2
            elif current < change2:
                a = 4
            elif current < change3:
                a = 3
            else:
                a = -5
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            if move < 0:
                move = 0
            current += round(move)
            track.append(round(move))


        error_time = 0
        while error_time < 10:
            track.append(1)
            error_time += 1
        while error_time > 0:
            track.append(-1)
            error_time -= 1

        '''
        time = 0
        while time < 100:
            track.append(0)
            time += 1
        i = 0
        while i < distance + 2:
            track.append(1)
            i += 1

        return track

    def locate_botton(self):
        return self.browser.find_element_by_class_name('geetest_slider_button')

    def drag_and_slide(self,button,track):
        ActionChains(self.browser).click_and_hold(button).perform()
        for x in track:
            print(str(x))
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        ActionChains(self.browser).release().perform()

    def does_element_exist(self,element):
        try:
            self.browser.find_element_by_class_name(element)
        except NoSuchElementException:
            return False
        else:
            return True

    def run(self):

        self.shoot_ver()
        botton = self.locate_botton()
        dis = self.get_track_length(pic_name)
        if dis == 404:
            self.browser.find_element_by_class_name('geetest_refresh_1').click()
            self.run()
        track = self.get_track(dis)
        time.sleep(2)
        print('实际上，我是第五层')
        self.drag_and_slide(botton,track)
        time.sleep(2)
        print('从现在开始，我要起飞')
        if self.does_element_exist('tit'):
            print('芜湖呼呼呼呼呼呼')
            self.browser.refresh()
            self.call_ver(self.username,self.pw)
            self.run()
        else:
            time.sleep(3)
            self.browser.close()

if __name__ == '__main__':
    crack = crack_bilibili_login()
    crack.open_login_page()
    crack.call_ver(user,password)
    crack.run()
