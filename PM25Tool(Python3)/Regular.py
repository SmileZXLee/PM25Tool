#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/PM25Tool'
import json
import re

def get_city_area(city_html):
	area_match = re.compile(r'<i>&bull;</i>(.*?)</a></li>')
	return area_match.findall(city_html)

def get_aqi_data(detail_html):
	detail_html = detail_html.replace('\n','').replace('\r','').replace('\t','').replace(' ','')
	aqi_data = re.compile(r'varoption_d30=(.*?);')
	return aqi_data.findall(detail_html)
	


