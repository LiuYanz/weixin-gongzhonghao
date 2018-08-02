# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
import urllib.request
from .cookies_key import cookies
import json
from weixin.items import WeixinItem
from scrapy.http import Request
from urllib.parse import urlparse,parse_qs
import requests
import random
import time

class WeixinSpiderSpider(scrapy.Spider):
    name = 'weixin_spider'
    allowed_domains = ['https://mp.weixin.qq.com']

    # 列表页面的api
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.7864539725247495&action=list_ex&begin=0&count=5&query=&fakeid=MzI4NzA5NjAwMQ%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.9413044088132714&action=list_ex&begin=0&count=5&query=&fakeid=MjM5NzMxODk4Mg%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.4354827667721499&action=list_ex&begin=0&count=5&query=&fakeid=MzA3Njg0MjgwNA%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=553621573&lang=zh_CN&f=json&ajax=1&random=0.4736710637827988&action=list_ex&begin=0&count=5&query=&fakeid=MzA3Njg0MjgwNA%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=553621573&lang=zh_CN&f=json&ajax=1&random=0.791663559016355&action=list_ex&begin=0&count=5&query=&fakeid=MzI5Nzk5OTM4NA%3D%3D&type=9'
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=553621573&lang=zh_CN&f=json&ajax=1&random=0.5152146683405507&action=list_ex&begin=0&count=5&query=&fakeid=MjM5MzA0MTg2MA%3D%3D&type=9'

    # 解析列表页面api接口
    def urls_fn(self,url_item=url):
        urls = []
        for i in range(1, 10):
            num = i * 5
            o = urlparse(url_item)
            query = parse_qs(o.query)
            random_num = '%.16f' % random.uniform(0.0000000000000001, 0.9999999999999999)
            query['random'][0] = random_num
            query['begin'][0] = num
            message = "&".join(u"{}={}".format(k, v[0]) for k, v in query.items())
            url_http = "https://mp.weixin.qq.com/cgi-bin/appmsg?"
            url = url_http + message
            urls.append(url)

        return urls

    start_urls = urls_fn(url)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, cookies=cookies, callback=self.parse_page)
            time.sleep(3)

    #列表页面
    def parse_page(self, response):

        if response:
            data = json.loads(response.text)
            # 输出data
            # print(data)

            # for app_msg_list in data['list']:
            for app_msg_list in data['app_msg_list']:
                item = WeixinItem()

                #标题
                # item['title'] = app_msg_list['nickname']
                item['title'] = app_msg_list['title']

                #修改时间
                item['update_time'] = app_msg_list['update_time']

                #文章链接
                item['link'] = app_msg_list['link']

                # yield item
                url = app_msg_list['link']

                bbb = []
                data = urllib.request.urlopen(url).read().decode('utf-8')
                content = re.compile('<div class="rich_media_content " id="js_content">.*?</div>', re.DOTALL)
                con = re.findall(content, data)
                cont = re.compile('>(.*?<)', re.DOTALL)
                contents = re.findall(cont, con[0])
                for i in contents:
                    if i != '' and i != '<' and i != '>' and i != '\\r' and i != '\\n' and i != "<'" and i != contents[0]:
                        bbb.append(i)
                item['contents'] = bbb
                time = re.compile('<em id="publish_time" class="rich_media_meta rich_media_meta_text">(.*?)</em>',
                                  re.DOTALL)
                tim = re.findall(time, data)
                item['time'] = tim

                # response = urllib.request.urlopen(url)
                #
                # item['contents'] = response.xpath('//*[@id="js_content"]/p/text()')
                # item['image'] = response.xpath('//*[@id="js_content"]/p/img/@src')

                yield item


class Spider(scrapy.Spider):
    name = 'ip'
    allowed_domains = []

    def start_requests(self):

        url = 'http://ip.chinaz.com/getip.aspx'

        for i in range(4):
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self,response):
        print(response.text)


