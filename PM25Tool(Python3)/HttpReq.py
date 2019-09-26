#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/PM25Tool'
import json
import requests
from requests.cookies import RequestsCookieJar
from urllib import *

def json_dic(json_str):
	json_object = json.loads(json_str)
	return json_object


def send_req(url,headers,data,remember_token,post_type):
	str_json = json.dumps(data)
	org_headers = {}
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



