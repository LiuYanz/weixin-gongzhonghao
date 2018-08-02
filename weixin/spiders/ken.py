
'''
这是测试用例
'''

import time
import requests
import json

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
    "Cookie" : "rewardsn=; wxtokenkey=777; wxuin=411171575; devicetype=Windows10; version=6206021b; lang=zh_CN; pass_ticket=BNKM3eeVl4pVB61oYdfUKMfAB54LcsYnT2dupvcSrryRe5JIfvBfdwYi8Q1oOr/1; wap_sid2=CPf1h8QBElxYZjhfRDJzUnlhS1AwZWZIRks3ZkwwUDZicWV3MlkwRDhBcDlkOTIyVWUwNWFaWmVSSkJLZGZ5WExOQlUxTFBWckE0VDZ6eWZBNVJLZmJpZDItV0RxcmtEQUFBfjCNyPLWBTgNQAE=",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.27.400 QQBrowser/9.0.2524.400"
}

# 添加data，`req_id`、`pass_ticket`分别对应文章的信息，从fiddler复制即可。不过貌似影响不大
data = {
	"__biz" : "MzUzNTcwNDkxNA==",
	"abtest_cookie":"",
	"appmsg_type" : "9",
	"both_ad" : "0",
	"comment_id" : "0",
	"ct" : "1524301200",
	"devicetype" : "Windows&nbsp;10",
	"idx" : "1",
	"is_need_ad" : "0",
	"is_need_reward" : "0",
	"is_need_ticket" : "0",
	"is_only_read" : "1",
	"is_original" : "0",
	"is_temp_url" : "0",
	"mid" : "2247484182",
	"msg_daily_idx" : "1",
	"pass_ticket" : "BNKM3eeVl4pVB61oYdfUKMfAB54LcsYnT2dupvcSrryRe5JIfvBfdwYi8Q1oOr%252F1",
	"r" : "0.6040599788539112",
	"req_id" : "22219NGqdgu78GNZHiJk7Dqr",
	"reward_uin_count" : "0",
	"scene" : "38",
	"send_time":"",
	"sn" : "29db4ce7996b5b61cc50482c29ae2adc",
	"title":"%E4%BB%A5%E5%89%8D%E7%83%A6%E6%81%BC%E9%9D%92%E6%98%A5%E7%97%98%EF%BC%8C%E7%8E%B0%E5%9C%A8%E7%83%A6%E6%81%BC%E5%B0%8F%E7%BB%86%E7%BA%B9",
	"version":""
	}

params = {
	"f" : "json",
	"uin" : "NDExMTcxNTc1",
	"key" : "11ebb00d5fe818881fc4d26ab284b0eee3a515b9d95ebab2be9f748ea37259999ed3b114d76e77fabd3e79facdc2b8fde86e0df810f354d1cef85366b9efc0e6a09eda7bd03840b5ba9bc2a4e7303932",
	"pass_ticket" : "BNKM3eeVl4pVB61oYdfUKMfAB54LcsYnT2dupvcSrryRe5JIfvBfdwYi8Q1oOr%252F1",
	"wxtoken" : "777",
	"devicetype" : "Windows&nbsp;10",
	"clientversion" : "6206021b",
	"appmsg_token" : "953_ucEzgSDLUI%2BPyWTRF9DLSYlVmTw0uEzaTcj4VgOyE_82wFzJhD7meE2JYiTP7iEzCC_gzRAZJMTSA-h1",
	"x5" : "0",
	}

# 使用post方法进行提交
content = requests.post(url, headers=headers, data=data, params=params).json()
print(content)

# 提取其中的阅读数和点赞数
# print(content["appmsgstat"]["read_num"], content["appmsgstat"]["like_num"])