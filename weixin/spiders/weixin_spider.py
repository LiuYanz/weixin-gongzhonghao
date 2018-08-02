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
    # url = "https://mp.weixin.qq.com/cgi-bin/appmsg?token=11025181&lang=zh_CN&f=json&ajax=1&random=0.3696024850392463&action=list_ex&begin=0&count=5&query=&fakeid=MzUzNTcwNDkxNA%3D%3D&type=9"
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=1139358760&lang=zh_CN&f=json&ajax=1&random=0.365358181520097&action=list_ex&begin=0&count=5&query=&fakeid=MzAwODE2OTAwNg%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.5344936554990483&action=list_ex&begin=0&count=5&query=&fakeid=MzAwODE2OTAwNg%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.7466239159466235&action=list_ex&begin=0&count=5&query=&fakeid=MzIxNTgyMDUzNA%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.5828173812745807&action=list_ex&begin=0&count=5&query=&fakeid=MzA3Mzg4NDYxMg%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.8666407736107136&action=list_ex&begin=0&count=5&query=&fakeid=MzIwMTQ0MzY2OA%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.24015679172233417&action=list_ex&begin=0&count=5&query=&fakeid=MzI5ODA4MjQ4NQ%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.3041637680414526&action=list_ex&begin=0&count=5&query=&fakeid=MzA3NTU1MzgyOA%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.01675267965183025&action=list_ex&begin=0&count=5&query=&fakeid=MjM5NzMyOTY2OA%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.4245464810582604&action=list_ex&begin=0&count=5&query=&fakeid=MzA3MjQ0NTMxNQ%3D%3D&type=9'
    # url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.41366324287372414&action=list_ex&begin=0&count=5&query=&fakeid=MzA3NTQxODUzMQ%3D%3D&type=9'
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




'''

                # 获取响应参数
                # o = urlparse(item['link'])
                # print(o)

                #获取响应参数
                o = urlparse(item['link'])
                query = parse_qs(o.query)
                sn = query['sn'][0]
                idx = query['idx'][0]
                mid = query['mid'][0]

                # 目标url
                url = "http://mp.weixin.qq.com/mp/getappmsgext"

                # 添加Cookie避免登陆操作，这里的"User-Agent"最好为手机浏览器的标识
                headers = {
                    "Host": "mp.weixin.qq.com",
                    "Connection": "keep-alive",
                    "Content-Length": "760",
                    "Accept": "*/*",
                    "CSP": "active",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://mp.weixin.qq.com",
                    "Cookie": "",#你的cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.27.400 QQBrowser/9.0.2524.400"
                }

                # post提交的参数
                data = {
                    "__biz": "MzUzNTcwNDkxNA==",
                    "is_only_read": "1",
                    "req_id": "22219NGqdgu78GNZHiJk7Dqr",#可变
                    "pass_ticket": 'BNKM3eeVl4pVB61oYdfUKMfAB54LcsYnT2dupvcSrryRe5JIfvBfdwYi8Q1oOr%252F1',#可变
                    "is_temp_url": "0",
                }

                # url参数使用 params
                params = {
                    "mid": mid,
                    "sn": sn,
                    "idx": idx,
                    "key": "11ebb00d5fe818881fc4d26ab284b0eee3a515b9d95ebab2be9f748ea37259999ed3b114d76e77fabd3e79facdc2b8fde86e0df810f354d1cef85366b9efc0e6a09eda7bd03840b5ba9bc2a4e7303932",
                    "pass_ticket": "BNKM3eeVl4pVB61oYdfUKMfAB54LcsYnT2dupvcSrryRe5JIfvBfdwYi8Q1oOr%252F1",#可变
                    "appmsg_token": "953_ucEzgSDLUI%2BPyWTRF9DLSYlVmTw0uEzaTcj4VgOyE_82wFzJhD7meE2JYiTP7iEzCC_gzRAZJMTSA-h1",#可变
                }

                #使用post方法进行提交
                # content = requests.post(url, headers=headers, data=data, params=params).json()
                # print(content)

                #阅读
                # item['read_num'] = content["appmsgstat"]["read_num"]

                #点赞
                # item['like_num'] = content["appmsgstat"]["like_num"]

                yield item
'''
'''
                                url = app_msg_list['link']

                                yield scrapy.Request(url=url,callback=self.parse_info,meta={'item':item})
                                # yield item

                    def parse_info(self, response):
                        item = response.meta['item']
                        item['contents'] = response.xpath('//*[@id="js_content"]/p/text()')
                        item['image'] = response.xpath('//*[@id="js_content"]/p/img/@src')
                        print(item['contents'])
                        yield item
'''

