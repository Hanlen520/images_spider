# -*- coding=utf-8 -*-
'''
网页下载器：访问传递过来的url，并将网页下载下载
1.对于web网页的加载机制ajax
2.安全机制（防代理，防爬虫）
3.cookie设置
'''
import urllib2
import chardet
from gzip import GzipFile
from StringIO import StringIO
import zlib
class HtmlDownloader(object):

    def download(self,url):
        if url is None:
            return None
        response = urllib2.urlopen(url)    #访问传送过来的url
        if response.getcode() != 200:      #如果访问的状态不是：200（成功），返回none
            return None
        print "download url:%s is ok" %url
        content = response.read()
        response.close()
        return content             #访问url后，将html内容下载下来，并返回回去

    def get_page(self,url):
        headers = {'Host': 'www.1fl.xyz',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cookie': 'M1fC_2132_saltkey=QhhqD8Rh; M1fC_2132_lastvisit=1479734501; M1fC_2132_atarget=1; M1fC_2132_visitedfid=2; M1fC_2132_forum_lastvisit=D_2_1479741018; M1fC_2132_sid=a8rrUH; M1fC_2132_lastact=1479823501%09home.php%09misc; M1fC_2132_sendmail=1; Hm_lvt_eb54d48e759ceecf0d6105086f52c0f5=1479738173,1479823572; Hm_lpvt_eb54d48e759ceecf0d6105086f52c0f5=1479823572'
            }

        if url is None:
            return None
        req = urllib2.Request(url,headers=headers)    #访问传送过来的url
        response = urllib2.urlopen(req)
        if response.getcode() != 200:      #如果访问的状态不是：200（成功），返回none
            return None
        cont = response.read()
        encoding = response.info().get('Content-Encoding')
        if encoding == 'gzip':
            try:
                buf = StringIO(cont)
                f = GzipFile(fileobj=buf)
                content = f.read()
            except:
                content = f.extrabuf   #未公开属性：extrabuf，负责保存已经成功解压的数
        elif encoding == 'deflate':
            try:
                content = zlib.decompress(cont, -zlib.MAX_WBITS)
            except zlib.error:
                content = zlib.decompress(cont)
        response.close()
        return content.decode("GB2312","ignore").encode("utf-8")
