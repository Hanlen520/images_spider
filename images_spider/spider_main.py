# -*- coding=utf-8 -*-
'''
广度爬取
'''
import url_manager, html_parser, html_outputer,html_downloader

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

if __name__ == "__main__":
    root_url = "http://www.1fl.xyz/forum-2-1.html"  #入口url:决定是否深度或广度
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)

