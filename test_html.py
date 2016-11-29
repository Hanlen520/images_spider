# -*- coding=utf-8 -*-
'''
广度爬取
'''

from images_spider import html_downloader, url_manager, html_outputer ,html_parser


import threading
import random
import time
import Queue

MAX_SIZE = 5
#模拟共享队列
URL_PRODUCER = set()
URL_CONSUMER = set()
CONDITION = threading.Condition()


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()     #初始化url管理器
        self.downloader = html_downloader.HtmlDownloader()  #初始化网页下载器
        self.parser = html_parser.HtmlParser()  #初始化网页解析器
        self.outputer = html_outputer.HtmlOutputer()   #初始化数据收集器

    def craw_page_urls(self):
        print "AAAAAA"
        global URL_PRODUCER
        global URL_CONSUMER
        while self.urls.has_new_url():
            # try:
            #获取新的资源
            wait_crawl_url = self.urls.get_new_url()
            wait_parse_html = self.downloader.get_page(wait_crawl_url)
            new_page_urls,new_image_urls = self.parser.parse(wait_crawl_url,wait_parse_html)

            #将新资源同步到队列中：线程内维护page的url
            abs_new_urls = self.urls.add_new_urls(new_page_urls)

            CONDITION.acquire()
            while True:
                if len(URL_CONSUMER) >= 50:
                    print "AAAAAA URL_PRODUCER is full.."
                    CONDITION.wait()
                    print "Consumer have comsumed something"
                else:
                    break

            if abs_new_urls is not None and len(abs_new_urls)>=1:
                for n in abs_new_urls:
                    URL_PRODUCER.add(n)
                print "P >>> " +str(len(URL_PRODUCER))

            if new_image_urls is not None and len(new_image_urls)>=1:
                for m in new_image_urls:
                    URL_CONSUMER.add(m)
                print "C <<< " +str(len(URL_CONSUMER))

            CONDITION.notify()
            CONDITION.release()
            time.sleep(random.random())
            # except Exception,e:
            #     print e
            #     print "crawl failed"

    def do_craw_work(self):
        print "BBBBBB"
        global URL_CONSUMER
        while True:
            CONDITION.acquire()
            while True:
                if not URL_CONSUMER or len(URL_CONSUMER)<1:
                    print "BBBBBB URL_CONSUMER is Empty..."
                    CONDITION.wait()
                    print "wait product"
                else:
                    break

            if len(URL_CONSUMER)>=1:
                print len(URL_CONSUMER)
                product = URL_CONSUMER.pop()
                b = self.outputer.output_one_jpg(product)
                if b:
                    URL_CONSUMER.add(product)

            CONDITION.notify()
            CONDITION.release()
            time.sleep(random.random())


if __name__ == "__main__":
    root_url = "http://www.1fl.xyz/forum-2-1.html"  #入口url:决定是否深度或广度
    obj_spider = SpiderMain()
    obj_spider.urls.add_new_url(root_url)

    threads = []

    # 创建新线程
    get_thread = threading.Thread(target=obj_spider.craw_page_urls, name='craw_page_urls')

    work_thread1 = threading.Thread(target=obj_spider.do_craw_work, name='do_craw_work1')
    work_thread2 = threading.Thread(target=obj_spider.do_craw_work, name='do_craw_work2')
    work_thread3 = threading.Thread(target=obj_spider.do_craw_work, name='do_craw_work3')
    work_thread4 = threading.Thread(target=obj_spider.do_craw_work, name='do_craw_work4')
    work_thread5 = threading.Thread(target=obj_spider.do_craw_work, name='do_craw_work5')

    # 开启新线程
    get_thread.start()

    work_thread1.start()
    work_thread2.start()
    work_thread3.start()
    work_thread4.start()
    work_thread5.start()

    # 添加线程到线程列表
    threads.append(get_thread)

    threads.append(work_thread1)
    threads.append(work_thread2)
    threads.append(work_thread3)
    threads.append(work_thread4)
    threads.append(work_thread5)

    # 等待所有线程完成
    for t in threads:
        t.join()

    print "Exiting Main Thread"



