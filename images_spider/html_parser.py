# -*- coding=utf-8 -*-
'''
网页解析器：对发送过来的html网页，解析出想要的内容
'''
from bs4 import BeautifulSoup
import re
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
class HtmlParser(object):

    def url_join(self,base, url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def _get_new_page_urls(self, page_url, soup):   #构造函数：在网页中获取新的url
        new_page_urls = set()
        # links = soup.find_all('a',href=re.compile(r'.*?\.html'))  #mimi
        links = soup.find_all('a',href=re.compile(r'.*?\/(forum|thread)-\d+?-\d+?-*?\d*?\.html')) #tuilvlang
        for link in links:
            new_url = link['href']
            if re.search(r'_',new_url):
                new_full_url = urljoin(page_url,new_url)
                new_page_urls.add(new_full_url)
            elif re.match(r'http',new_url):
                new_page_urls.add(new_url)
        return new_page_urls

    def _get_new_image_urls(self, html, soup):    #构造函数：在网页中获取新的数据
        #<img id="aimg_683" aid="683" src="data/attachment/forum/201601/26/124630djpnnkwkpfvjgnyc.jpg" zoomfile="data/attachment/forum/201601/26/124630djpnnkwkpfvjgnyc.jpg" file="data/attachment/forum/201601/26/124630djpnnkwkpfvjgnyc.jpg" class="zoom" onclick="zoom(this, this.src, 0, 0, 0)" width="850" inpost="1" onmouseover="showMenu({'ctrlid':this.id,'pos':'12'})" data-bd-imgshare-binded="1" initialized="true">
        new_image_urls = []
        image_urls = soup.find_all('img',file=re.compile(r'^data\/attachment\/forum\/\d+?\/.*?\.jpg'))
        for link in image_urls:
            new_url = link['file']
            full_url = urljoin("http://www.1fl.xyz/", new_url)
            new_image_urls.append(full_url)
        return new_image_urls
        '''
        re_m = r'<img src="(.*?\.jpg)" alt=".*?" width=".*?" height=".*?" />'
        re_m_t = r'<img alt=".*?" src="(.*?\.jpg)" />'
        reg = re.compile(re_m)
        reg_t = re.compile(re_m_t)
        new_image_urls = re.findall(reg,html)
        new_image_urls_t = re.findall(reg_t,html)
        new_image_urls.extend(new_image_urls_t)
        return new_image_urls
        '''
    def parse(self,wait_crawl_url,wait_parse_html):     #使用BeautifulSoup第三方网页解析器
        if wait_crawl_url is None or wait_parse_html is None:
            return
        soup = BeautifulSoup(wait_parse_html,'html.parser',from_encoding='utf-8')
        new_page_urls = self._get_new_page_urls(wait_crawl_url,soup)
        new_image_urls = self._get_new_image_urls(wait_parse_html,soup)
        return new_page_urls,new_image_urls


