#coding=utf-8
__author__ = 'zxlee'
import json
import requests
from requests.cookies import RequestsCookieJar
import urlparse

def json_dic(json_str):
	try:
		json_object = json.loads(json_str)
	except ValueError, e:
		json_object = {}
	return json_object


def send_req(url,headers,data,remember_token,post_type):
	str_json = json.dumps(data)
	up = urlparse.urlparse(url)
	org_headers = {
		"Accept": "*/*",
		"Accept-Encoding": "br, gzip, deflate",
		"Accept-Language": "zh-Hans-CN;q=1",
		"Connection": "keep-alive",
		"Host": up.netloc,
		"User-Agent": "Test/1.1.8 (iPhone; iOS 12.1.2; Scale/3.00)"
	}
	final_headers = org_headers.copy()
	if headers :
		final_headers.update(headers)

	cookie_jar = RequestsCookieJar()
	if len(remember_token):
		cookie_jar.set("remember_token",remember_token, domain=up.netloc)
	if post_type.upper() == 'POST':
		res = requests.post(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	elif post_type.upper() == 'PUT':
		res = requests.put(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	elif post_type.upper() == 'GET':
		res = requests.get(url)
	else:
		print('TypeErr')
	return res.text



