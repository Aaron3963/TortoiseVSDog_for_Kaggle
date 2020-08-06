# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 12:43:40 2020

@author: James
"""
import requests
import re
 
 
def image_urls():
    search_name = "tortoise"
    search_num = 60
    # url存放的总列表
    all_urls = list()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    # query参数的值是要搜多的图片名，start参数的值是图片开始的下标
    for i in range(0, search_num*48, 48):
        print("搜索第{}页/{}...".format(int(i/48),search_num))
        url = 'https://pic.sogou.com/pics?query={0}&mode=1&start={1}&reqType=ajax&reqFrom=result&tn=0'.format(search_name, i)
        response = requests.get(url, headers=headers)
        url_list = re.findall('"thumbUrl":"(.*?)"', response.text)
        # 输入的关键字没有寻找到图片时
        if len(url_list) == 0:
            print("没有图片了")
        all_urls.extend(url_list)
        #删除重复的下载链接
    result_urls=[]
    for url in all_urls:
        if url not in result_urls:
            result_urls.append(url)
        else:
            print("删除重复的下载链接...")
    print("总共{}个下载链接".format(len(result_urls)))
        
    download(result_urls, headers)
 
 
def download(url_list, headers):
    count = 0
    for url in url_list:
        response = requests.get(url, headers=headers)
        with open('D:/2019CNN/sougou/%s.jpg' % count, 'ab') as f:
            f.write(response.content)
        print("下载保存第{}个...".format(count))
        count += 1
 
 
if __name__ == '__main__':
    image_urls()
