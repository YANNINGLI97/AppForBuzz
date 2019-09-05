import os
import time
import urllib
import requests
from scrapy import Selector
from selenium import webdriver


class GoogleImgCrawl:
    def __init__(self):
        self.browser = webdriver.Chrome('F:\chromedriver.exe')
        self.browser.maximize_window() #maxmize the window
        self.key_word = input('Please input the key words of the picture you want to grab >:')
        self.nums = input('Please input the number of the picture you want to grab >:')
        self.img_path = r'D:\GoogleImgDownLoad\%s' % self.key_word   # Downloads the pictures to local path
        if not os.path.exists(self.img_path):  # Create a folder when it it not exist
            os.makedirs(self.img_path)

    def start_crawl(self):
        self.browser.get('https://www.google.com/search?q=%s' % self.key_word + '&source=lnms&tbm=isch')
        self.browser.implicitly_wait(3)
        time.sleep(3)  # wait for loading
        img_source = self.browser.page_source
        img_source = Selector(text=img_source)
        self.img_down(img_source)  # download tha pic
        self.slide_down()  # get more pic

    def slide_down(self):

        for i in range(7, 100):  # set the range you need
            pos = i * 800
            js = "document.documentElement.scrollTop=%s" % pos
            self.browser.execute_script(js)
            time.sleep(3)
            if int(i) == 20:
                print(self.browser.page_source)
            img_source = Selector(text=self.browser.page_source)
            try:
                self.img_down(img_source)
            except BaseException as e:
                print(e)


    def img_down(self, img_source):
        img_url_list = img_source.xpath('//div[@class="THL2l"]/../img/@src').extract()
        for each_url in img_url_list:
            if 'https' not in each_url:
                # print(each_url)
                each_img_source = urllib.request.urlretrieve(each_url,
                                                             '%s/%s.jpg' % (self.img_path, time.time())) # download the picture
            else:
                response = requests.get(each_url, verify=True)
                with open('D:\GoogleImgDownLoad\%s.jpg' % time.time(), 'wb')as f:
                    f.write(response.content)
            self.nums = int(self.nums) - 1  # termination condition
            print(self.nums)
            if self.nums == 0:
                exit()



if __name__ == '__main__':
    google_img = GoogleImgCrawl()
    google_img.start_crawl()
