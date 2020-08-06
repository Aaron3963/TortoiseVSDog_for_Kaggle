#-*- coding: utf-8 -*-
"""
Created on Tue Feb 11 22:05:39 2020

@author: James
"""

#*******本脚本运行时需要本机安装 Chrome 浏览器以及Chrome的驱动，同时需要selenium库的支撑********
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import os,time  
import requests
from bs4 import BeautifulSoup as bs
import re  

#****************************************************
base_url_part1 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
base_url_part2 = '&oq=bagua&rsp=0' # base_url_part1以及base_url_part2都是固定不变的，无需更改
search_query = 'tortoise' # 检索的关键词，可自行更改
location_driver = 'D:/丘成桐竞赛/Codes/chromedriver.exe' # Chrome驱动程序在电脑中的位置

 
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
		for i in range(5000): # 此处可自己设置爬取范围，本处设置为1，那么不会有下滑出现
			pos += 100 # 每次下滚500  
			js = "document.documentElement.scrollTop=%d" %pos    
			driver.execute_script(js)  
			time.sleep(2)
			# 获取页面源码
			html_page = driver.page_source
			# 利用Beautifulsoup4创建soup对象并进行页面解析
			soup = bs(html_page, "html.parser")
			# 通过soup对象中的findAll函数图像信息提取
			imglist = soup.findAll('img', {'src':re.compile(r'https:.*\.(jpg|png)')})
 
			for imgurl in imglist:
				result=imgurl['src']
				if result not in img_url_dic:
					try:
						img_url_dic.append(result)
						pic=requests.get(result, timeout=10)
						print("tort"+"_"+str(x)+'图片下载中...')	
						file_name="tort"+"_"+str(x)+".jpg"
						dir=os.path.join("./baidu",file_name)
						fp = open(dir, 'wb')
						fp.write(pic.content)
						fp.close()
						x += 1 					                                                
						time.sleep(1)
					except:
						print('当前图片无法下载')
						continue
                    
				else:
					print('重复的图片地址：{}'.format(result))
			

	def run(self):
		print ('\t\t\t**************************************\n\t\t\t**\t\tWelcome to Use Spider\t\t**\n\t\t\t**************************************')  
		driver=self.start_brower()
		self.downloadImg(driver)
		driver.close()
		print("Download has finished.")
 
if __name__ == '__main__':  
	craw = Crawler() 
	craw.run()
