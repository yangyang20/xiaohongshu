import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import re
import pymysql
from selenium.webdriver.chrome.options import Options
import json
import os


opts = Options()
# opts.headless = True
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--headless')
opts.add_argument('blink-settings=imagesEnabled=false')
opts.add_argument('--disable-gpu')
drive_path = 'chromedriver.exe'

class XiaoHongShu:

    def __init__(self,id,url=''):
        if url == '':
            self.baseUrl = f'https://www.xiaohongshu.com/discovery/item/{id}'
        else:
            self.baseUrl = url
        self.data = {}
        self.requestUrl()


    def requestUrl(self):

        driver = webdriver.Chrome(executable_path=drive_path, options=opts)
        # url = baseUrl + '60500ecf000000002103f257'

        # self.data['xiaohongshu_id'] = id
        driver.get(self.baseUrl)
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "slide")))
        html = driver.find_element_by_id('app').get_attribute('innerHTML')
        self.parseHtml(html)
        driver.close()

    def parseHtml(self,html):
        doc = pq(html)
        imageList = doc('.slide li span')
        imageUrl = []
        for item in imageList.items():
            style = item.attr('style')
            temp = re.findall(r'\/\/(.*)\/', style)[0]
            imageUrl.append('http://'+temp + '.jpg')

        self.data['images'] = imageUrl
        print(imageUrl)

        titleDoc = doc('h1.title')
        title = titleDoc.text()
        self.data['title'] = title
        print(title)

        contentList = []
        contentDoc = doc('.all-tip .content p')
        for item in contentDoc.items():
            contentList.append(item.text())
        self.data['content'] = contentList
        print(contentList)


    def download(self):
        imageList = self.data['images']
        title = self.data['title']
        contentList = self.data['content']
        i = 1
        path = f'./{title[0:4]}'
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        for url in imageList:
            r = requests.get(url)
            if r.status_code == 200:
                imagePath = f'{path}/{i}.jpg'
                open(f'{imagePath}', 'wb').write(r.content)  # 将内容写入图片
                i+=1
        f = open(f'{path}/content.txt', 'a',encoding='utf-8')
        f.write(str(title) +'\n')
        for item in contentList:
            f.write(str(item) + '\n')
        f.close()


    def insertData(self):
        # 获取游标
        connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='393622951',
                                 db='dream_home',
                                 charset='utf8')
        cursor = connection.cursor()
        images = json.dumps(self.data['images'])
        content = json.dumps(self.data['content'])
        sql = f'''
                 INSERT INTO `xiaohongshu`
                 (`xiaohongshu_id`, `images`,`title`,`content`) VALUES
                 ('{self.data['xiaohongshu_id']}','{images}','{self.data['title']}','{content}')
                 '''
        print(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    xiaohongshu = XiaoHongShu('60500ecf000000002103f257')
    xiaohongshu.download()








