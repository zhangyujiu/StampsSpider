# -*- coding: utf-8 -*-

import os
from urllib import request
from lxml import etree


class Spider(object):
    def __init__(self):
        self.path = "./images/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.baseUrl = "http://chinesestamps.info/jfzz"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }

    def load_page(self):
        req = request.Request(self.baseUrl, headers=self.headers)
        rsp = request.urlopen(req)
        html = rsp.read()
        html = etree.HTML(html)
        results = html.xpath('//div[@id="wrapper"]/div[@id="content"]/p/a/@href')
        return results

    def load_child_page(self, path):
        req = request.Request(path, headers=self.headers)
        rsp = request.urlopen(req)
        html = rsp.read()
        html = etree.HTML(html)
        title = html.xpath('//div[@class="post"]/h2[@class="posttitle"]/a/text()')
        images = html.xpath('//div[@class="postentry"]/p/a/@href')
        return title[0].split(' ')[0], images

    def download_image(self, path, title):
        try:
            req = request.Request(path, headers=self.headers)
            rsp = request.urlopen(req)
            html = rsp.read()

            suffix = str(path).split('.')[-1]
            print("正在存储文件 %s.%s" % (title, suffix))
            file_path = self.path + title + "." + str(suffix)
            if not os.path.exists(file_path):
                file = open(file_path, 'wb')
                file.write(html)
                file.close()
        except request.HTTPError:
            print("----404----")


if __name__ == "__main__":
    spider = Spider()
    results = spider.load_page()
    for result in results:
        title, images = spider.load_child_page(result)
        for image in images:
            spider.download_image(image, title)
