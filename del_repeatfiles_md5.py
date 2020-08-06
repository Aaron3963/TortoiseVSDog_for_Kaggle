# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 22:30:58 2020

@author: James
在原来md5方法的基础上，对于尺寸在800*600之内的图片，再增加一个略缩图到80*60，查重功能

"""
import hashlib
import os,time
from PIL import Image
import base64
from io import BytesIO

def getmd5(filename):
    file_txt = open(filename,'rb').read()
    m = hashlib.md5(file_txt)
    return m.hexdigest()

def main():
    #path = "E:\CNN\Dataset\Tortoise"
    path = "E:\CNN\Dataset\Dog"
    #path = "E:\CNN\Tortoise"
    #path = "d:\CNN\OIDv4\Images_OIDv4"
    for dirpath,dirnames,filenames in os.walk(path):
        if dirpath == path:
            img_files_list=filenames

    total_images=len(img_files_list)
    print('总共{}个图像文件'.format(total_images))
    
    all_md5=[]
    total_delete=0
    
    print("--"*20)
    print("两种方法一起删除重复文件，处理中...")
    time_start=time.time()
    for file in img_files_list:
        real_path=os.path.join(path,file)
        filemd5=getmd5(real_path)
        if filemd5 in all_md5:
            total_delete += 1
            print ('通过MD5删除重复文件：',file)
            os.remove(real_path)
        else:
            all_md5.append(filemd5)

    print('开始第二阶段查重')
    all_thumbnail_md5=[]
    width_height_tuple=(80,60)
    for dirpath,dirnames,filenames in os.walk(path):
        if dirpath == path:
            img_files_list=filenames
     
    for file in img_files_list:
        src = os.path.join(path, file)
        img = Image.open(src)
        img.thumbnail(width_height_tuple, Image.ANTIALIAS)#生成略缩图
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)#base64编码生成字符串
        img_md5 = hashlib.md5(base64_str)        
        if img_md5 in all_thumbnail_md5:
            total_delete += 1
            print ('通过thumbnail删除重复文件：',file)
            os.remove(src)
        else:
            all_thumbnail_md5.append(img_md5)

    time_spend=time.time()-time_start
    print ('总共删除个数：',total_delete)
    print ('剩余个数：',total_images-total_delete)    
    print("Total spend time: {:.1f} minutes!".format(time_spend/60))
     
if __name__=='__main__': 
    main()
