# -*- coding=utf-8 -*-
'''
url管理器：主要管理网页中新获取的url，和已经爬取过的url
'''
import re

class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self,url):     #将新的url添加到new_urls中
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
        return self.new_urls

    def has_new_url(self):
        return len(self.new_urls) != 0   #如果等于0  就是没有

    def get_new_url(self):              #将爬取过的url添加到old_urls中
        for s in self.new_urls:
            if re.search(r"_",s):
                self.new_urls.remove(s)   #将set中的数据读出并删除set中的数据
                self.old_urls.add(s)
                return s
        new_url = self.new_urls.pop()   #将set中的数据读出并删除set中的数据
        self.old_urls.add(new_url)
        return new_url
