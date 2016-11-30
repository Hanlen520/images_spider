# images_spider
just for me

本项目使用了一下python相关的模块
    1.threading   #多线程开启网页下载和图片下载同时进行
      random
      time
      Queue       #设计师使用set()数据类型代替了Queue
    5.urllib      #这三个主要是用于下载资源用的
      urllib2
      requests
    9.chardet     #查看资源的编码类型
    10.gzip.GzipFile     #网络资源在请求后返回的数据形式为gzip或其他时，由其处理
      zlib
    12.StringIO /cStringIO
    13.os
    14.PIL.Image      #处理图片时使用的
    15.bs4.BeautifulSoup     #对网页进行解析
    16.re
    17.urlparse.urljoin   #对url进行解析和处理的
       urlparse.urlparse
       urlparse.urlunparse
       posixpath.normpath


逻辑：
1.通过url进入到网络中，对指定url的网络资源进行下载，并进行业务分析（所需要的数据类型或格式）
2.渗透到网络服务器中将网站的资源进行本地化
3.适用所有的网络图片爬取

