# -*- coding=utf-8 -*-
'''
广度爬取
'''
from images_spider import url_manager, html_parser, html_outputer,html_downloader
import threading
import random
import time
import Queue

MAX_SIZE = 5
SHARE_Q = []  #模拟共享队列
url_producer = []
CONDITION = threading.Condition()


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()     #初始化url管理器
        self.downloader = html_downloader.HtmlDownloader()  #初始化网页下载器
        self.parser = html_parser.HtmlParser()  #初始化网页解析器
        self.outputer = html_outputer.HtmlOutputer()   #初始化数据收集器

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                wait_crawl_url = self.urls.get_new_url()
                wait_parse_html = self.downloader.get_page(wait_crawl_url)
                new_page_urls,new_image_urls = self.parser.parse(wait_crawl_url,wait_parse_html)
                self.urls.add_new_urls(new_page_urls)
                b = self.outputer.collect_image_url(new_image_urls,200)
                if b == False:
                    break
            except Exception,e:
                print e
                print "crawl failed"
        self.outputer.output_jpg()

    def craw_page_urls(self):
        while self.urls.has_new_url():
            try:
                wait_crawl_url = self.urls.get_new_url()
                wait_parse_html = self.downloader.get_page(wait_crawl_url)
                new_page_urls,new_image_urls = self.parser.parse(wait_crawl_url,wait_parse_html)
                self.urls.add_new_urls(new_page_urls)
                b = self.outputer.collect_image_url(new_image_urls,200)
                if b == False:
                    break
            except Exception,e:
                print e
                print "crawl failed"

    def do_craw_work(self):
        global url_producer
        while True:
            CONDITION.acquire()
            if not url_producer :
                print "Queue is Empty..."
                CONDITION.wait()
                print "Producer have producted something"
            product = url_producer.pop(0)
            print "Consumer :", product
            self.outputer.output_one_jpg(product)
            CONDITION.notify()
            CONDITION.release()
            time.sleep(random.random())


if __name__ == "__main__":
    root_url = "http://www.1fl.xyz/forum-2-1.html"  #入口url:决定是否深度或广度
    obj_spider = SpiderMain()
    obj_spider.urls.add_new_url(root_url)
    obj_spider.craw(root_url)

