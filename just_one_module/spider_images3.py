#coding=utf-8

import re
import urllib
import os

#目的网址url

url = ""
thame = []
images_num = 1
#获取目的网页的html源码
def get_html(url):
    html = urllib.urlopen(url).read()
    return html

#获取每个主题的url
def get_pages(url):
    global url_list
    html = get_html(url)
    page_re = r'<a target="_blank" href="(.*?\.html)">'
    reg = re.compile(page_re)
    lsit = re.findall(reg,html)
    thame.extend(lsit)

#通过每个主题下获取主题下的链接
def get_thame_urls(thame_url):
    html = get_html(thame_url)
    thame_re = r'''<a href='([\d]*?\_[\d]*?\.html)' class="page-en">'''
    reg = re.compile(thame_re)
    thame_url_list = re.findall(reg,html)
    return thame_url_list

def get_image(url,abs_path_images):
    global images_num
    html = get_html(url)
    re_m = r'<img alt=".*?" src="(.*?\.jpg)" />'
    reg = re.compile(re_m)
    image_url = re.findall(reg,html)
    if image_url:
        for key in image_url:
#            image_name = os.path.basename(key)
            urllib.urlretrieve(key, abs_path_images + "\\%s.jpg" %images_num )
            print "      crawled %s pictures      " %images_num
            images_num+=1


#循环获每一页的主题
for i in range(2,63):
    if(i>2):
        url_add = "/xinggan/list_6_%s.html" %i
        get_pages(url_add)
    else:
        get_pages(url)
thame_num = 1
abs_path = os.getcwd()
abs_path_images = abs_path+"\\iamges3"
if not os.path.exists(abs_path_images):
    os.mkdir(abs_path_images)
fo = open("image_url2.txt",'a+')
num = 0
for thame_url in thame:
    if(thame_num < 10):
        print "    ====== this %s of thames ======" %thame_num
        iamge_list = get_thame_urls(thame_url)
        thame_num+=1
        thame_image_urls_num = len(iamge_list)
        print "====== this topic has %s pictures ======" %thame_image_urls_num
        for l in iamge_list:
            wait_image_url = "%s" %l
            fo.write(wait_image_url+'\n')
            get_image(wait_image_url,abs_path_images)
    else:
        print "    ====Crawl sexy pictures successfully,a total of %s====    " %images_num
        print "    ========================================================"
        break
fo.close()

