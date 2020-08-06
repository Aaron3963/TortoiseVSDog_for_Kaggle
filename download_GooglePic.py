#-*- coding: utf-8 -*-
"""
Created on Tue Feb 11 22:05:39 2020

@author: James
"""

#*******本脚本运行时需要本机安装 Chrome 浏览器以及Chrome的驱动，同时需要selenium库的支撑********
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time  
from bs4 import BeautifulSoup as bs
import re  
import os
import requests
import random

#****************************************************
base_url_part1 = 'https://www.google.com/search?q='
base_url_part2 = '&source=lnms&tbm=isch' # base_url_part1以及base_url_part2都是固定不变的，无需更改
search_query ="Костенурка" #检索的关键词，可自己输入你想检索的关键字，还可以多种语言
location_driver = 'E:/software/chromedriver.exe' # Chrome驱动程序在电脑中的位置


class Crawler:
	def __init__(self):
		self.url = base_url_part1 + search_query + base_url_part2

	# 启动Chrome浏览器驱动
	def start_brower(self):
		chrome_options = Options()
		chrome_options.add_argument("--disable-infobars")
		# 启动Chrome浏览器  
		driver = webdriver.Chrome(executable_path=location_driver, chrome_options=chrome_options)  
		# 最大化窗口，因为每一次爬取只能看到视窗内的图片
		driver.maximize_window()  
		# 浏览器打开爬取页面  
		driver.get(self.url)  
		return driver

	def downloadImg(self, driver):  

		# 记录下载过的图片地址，避免重复下载
		img_url_dic=[]

		x = 0  
		# 当鼠标的位置小于最后的鼠标位置时,循环执行
		pos = 0     
		for i in range(100): # 此处可自己设置爬取范围，本处设置为1，那么不会有下滑出现
			pos += random.randint(300,600)
			#pos +=500# 每次下滚500
			print("--"*30)
			print("第{}次爬, pos={}".format(i,pos))
			js = "document.documentElement.scrollTop=%d" %pos
			driver.execute_script(js)
			time.sleep(30)
			# 获取页面源码
			html_page = driver.page_source
			# 利用Beautifulsoup4创建soup对象并进行页面解析
			soup = bs(html_page, "html.parser")
			# 通过soup对象中的findAll函数图像信息提取
			imglist = soup.findAll('img', {'class':'rg_i'})
			#imglist = soup.findAll(class_=re.compile("rg_i"))
			num=len(imglist)
			print('find total image links: ' + str(num))
			#for i in range(len(imglist)):
			#	print("第{}个:{}".format(i,imglist[i]))
			#分两类进行处理：1.一部分采用data-iurl;一部分采用data-src
			for imgurl in imglist:
				attrs_dic=imgurl.attrs#提取属性，转化为字典，分类处理
				if attrs_dic.__contains__("data-iurl"):
					result=attrs_dic["data-iurl"]
				elif attrs_dic.__contains__("data-src"):
					result=attrs_dic["data-src"]
				#print(result)
				if result not in img_url_dic:
					try:
						img_url_dic.append(result)
						pic=requests.get(result, timeout=10)
						print(result)
						print("tort"+"_"+str(x)+'图片下载中...')	
						file_name="tort"+"_"+str(x)+".jpg"
						dir=os.path.join("./Download_google",file_name)
						fp = open(dir, 'wb')
						fp.write(pic.content)
						fp.close()
						x +=1
						time.sleep(1)
					except:
						print('当前图片无法下载')
						continue

				else:
					print('重复的图片地址：{}'.format(result))


	def run(self):
		print('\t\t\t**************************************\n\t\t\t**\t\tWelcome to Use Spider\t\t**\n\t\t\t**************************************')  
		driver=self.start_brower()
		self.downloadImg(driver)
		driver.close()
		print("Download has finished.")


if __name__ == '__main__':
	craw = Crawler() 
	craw.run()
