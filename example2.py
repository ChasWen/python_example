import requests
import os
import time
import threading
from bs4 import BeautifulSoup

j = 0  # 用于计数下载失败的数量

def download_page(url):
   '''
   用于下载页面
   '''
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20220715 Firefox/61.0"}
   r = requests.get(url, headers=headers)
   r.encoding = 'UTF-8'
   return r.text


def get_pic_list(html):
   '''
   获取每个页面的套图列表,之后循环调用get_pic函数获取图片
   '''
   soup = BeautifulSoup(html, 'html.parser')
   pic_list = soup.find('main', id='site-content').find_all('h2')
   for i in pic_list:
       link = i.find('a').get('href')  # 套图链接
       text = i.get_text()  # 套图名字
       sign = ['\\', '/', ':', '*', '？', '\"', '<', '>', '|']
       for i in sign:
          text = text.replace(i,'')
          get_pic(link, text)

def get_pic(link, text):
   global j
   '''
   获取当前页面的图片,并保存
   '''
   html = download_page(link)  # 下载界面
   soup = BeautifulSoup(html, 'html.parser')
   pic = soup.find('article')  # 找到界面图片区域
   pic_list = pic.findAll('img')
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
   }

   create_dir('pic/{}'.format(text))
   k = 1 # 用于图片命名
   for i in pic_list:
       pic_link = i.get('data-lazy-src')  # 拿到图片的具体 url
       if pic_link == None:
           continue;
       r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
       if r.status_code == 200:
           data = r.content
           f = open('pic/{}/{}{}'.format(text, k, '.png'), "wb")
           f.write(data)
           f.close()
           k = k+1
           time.sleep(1)
       else:
           j = j+1
           continue;

def create_dir(name):
   if not os.path.exists(name):
       os.makedirs(name)

def execute(url):
   page_html = download_page(url)
   get_pic_list(page_html)

def main():
   create_dir('pic')
   queue = [i for i in range(1, 9)]   # 构造 url 链接 页码。
   threads = []
   while len(queue) > 0:
       for thread in threads:
           if not thread.is_alive():
               threads.remove(thread)
       while len(threads) < 5 and len(queue) > 0:   # 最大线程数设置为 5
           cur_page = queue.pop(0)
           url = 'http://www.rxsy.net/category/gallery/shashin/page/{}'.format(cur_page)
           thread = threading.Thread(target=execute, args=(url,))
           thread.setDaemon(True)
           thread.start()
           print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
           threads.append(thread)

if __name__ == '__main__':
    main()
    # get_pic('http://www.rxsy.net/2021/11/little-light-by-aaronsky/','泛光 – 安静放松的美感')
    print('下载失败的数量为%d' %j)
