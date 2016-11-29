# -*- coding=utf-8 -*-
'''
数据收集器：将传送过来的数据，进行html格式的封装
'''
import os
import urllib
import requests
from PIL import Image
from StringIO import StringIO
import time
class HtmlOutputer(object):
    def __init__(self):
        self.images_lists = []    #创建一个list，收集数据

    def collect_image_url(self,images_list,num):    #如果发送过来的数据，不为空，就将数据添加到datas中
        if images_list is None:
            print "images_list is None"
            return
        #print "collect_image_url were :: %d" %(len(self.images_lists))
        self.images_lists.extend(images_list)  #list的拼接
        if len(self.images_lists) >= num:
            return False

    def output_jpg(self):
        # abs_path = os.getcwd()
        abs_path_images = "W:\\ththt\\iamges5"
        if not os.path.exists(abs_path_images):
            os.mkdir(abs_path_images)
        images_num = 1
        fo = open("image_urls5.txt",'a+')
        print "\n total image urls is %d \n" %(len(self.images_lists))
        if self.images_lists:
            for image_url in self.images_lists:
                #print "image_url is :: %s" %image_url
                fo.write(image_url+'\n')
                self.get_sources(image_url, abs_path_images + "\\%s.jpg" %images_num )
                print " ... crawled %s pictures ..." %images_num
                images_num+=1
        print "\n success crawled"
        fo.close()

    def output_one_jpg(self,image_url):
        abs_path_images = "W:\\ththt\\iamges5"
        if not os.path.exists(abs_path_images):
            os.makedirs(abs_path_images)
        fo = open("image_urls5.txt",'a+')
        fo.write(image_url+'\n')
        image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        self.get_sources(image_url, abs_path_images + "\\%s.jpg" %image_name )
        fo.close()
        return True

    def get_sources(self,url,filename):
            '''
            下载资源的三种方式：
            1.urllib.urlretrieve()
            2.urllib2.open() --> with open(,"wb") as f : f.write(r.read())
            3.request.open() --> with open(,"wb") as f : f.write(r.read())
                             --> PIL.Image.open(StringIO(r.read())).save("path.jpg")
            '''
            cont = requests.get(url)  #bytes
            if cont.status_code != 200:
                print "download error at get_sources func"
                return None
            image_content = Image.open(StringIO(cont.content))
            image_content.save(filename)
            image_content.close()
