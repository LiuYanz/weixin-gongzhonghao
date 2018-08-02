
'''
这是测试用例
'''


from urllib.parse import urlparse,parse_qs
import random

#列表页面的api
# url = "https://mp.weixin.qq.com/cgi-bin/appmsg?token=1251483713&lang=zh_CN&f=json&ajax=1&random=0.3696024850392463&action=list_ex&begin=0&count=5&query=&fakeid=MzUzNTcwNDkxNA%3D%3D&type=9"
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token=416364688&lang=zh_CN&f=json&ajax=1&random=0.5344936554990483&action=list_ex&begin=0&count=5&query=&fakeid=MzAwODE2OTAwNg%3D%3D&type=9'
#解析列表页面url
def urls_fn(item):
	urls = []
	for i in range(1,10):
		num = i*5
		o = urlparse(item)
		query = parse_qs(o.query)
		random_num = '%.16f' % random.uniform(0.0000000000000001,0.9999999999999999)
		query['random'][0] = random_num
		query['begin'][0] = num
		message = "&".join(u"{}={}".format(k,v[0]) for k,v in query.items())
		url_http = "https://mp.weixin.qq.com/cgi-bin/appmsg?"
		url = url_http + message
		urls.append(url)
	print(urls)
	return urls

if __name__ == '__main__':
	urls_fn(url)