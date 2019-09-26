#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/PM25Tool'
import json
import time
import HttpReq
import Regular
import sys
import os
import platform
from dateutil.parser import parse
import demjson
import re
from xlwt import *
import datetime

#是否是Windows
os_is_windows = platform.system() == 'Windows'

all_req_data = ['aqi','pm2_5','pm10','so2','no2','co','o3']
#程序入口
def main():
	print(u'欢迎使用PM25Tool-By照相')
	while (True):
		citys = get_citys()['citys'].split('#')
		print(u'任务开始！')
		for city in citys:
			city = city.strip()
			res = HttpReq.send_req('http://www.pm25.com/city/mon/aqi/%s.html'%(city),{},'','','GET')
			match_group = Regular.get_city_area(res)
			area_count = len(match_group) - 1
			if area_count == 0:
				print(u'未获取到[%s]的地区信息，自动跳过!'%city)
				continue
			if city in match_group:
                                
				area_count = area_count - 1
			print(u'%s共%d个地区，开始获取数据...'%(city,area_count))
			w = Workbook()
			for area in match_group:
				if area != u'返回' and area != city:
					print(u'开始获取[%s]的各项信息...'%area)
					ws = w.add_sheet(area)
					colData = []
					for interface in all_req_data:
						res = HttpReq.send_req('http://www.pm25.com/city/mon/%s/%s/%s.html'%(interface,city,area),{},'','','GET')
						aqi_datas = Regular.get_aqi_data(res)
						for aqi_data in aqi_datas:
							#aqi_data = Regular.adjust_json(aqi_data)
							aqi_json = demjson.decode(aqi_data)
							xdata = []
							new_xdata = []
							series = []
							if 'xAxis' in aqi_json:
								xdata = aqi_json['xAxis'][0]['data']
							if 'series' in aqi_json:
								series = aqi_json['series']

							for day in xdata:
								days = re.findall('\d+',day)
								if(len(days) > 0):
									day = str(days[0].encode('utf-8'))
									day = day.replace('b\'','').replace('\'','')
								new_xdata.append(day)
							new_xdata.insert(0,'')
							if(interface == 'aqi'):
								aqi1 = series[0]['data']
								aqi2 = series[1]['data']
								aqi1.insert(0,'America AQI')
								aqi2.insert(0,'China AQI')
								colData.append(new_xdata)
								colData.append(aqi1)
								colData.append(aqi2)
							else:
								aqi1 = series[0]['data']
								aqi1.insert(0,interface)
								colData.append(aqi1)
					add_to_excel(ws,area,colData)
			save_path = 'datas/%s-%s.xls'%(city,datetime.date.today().strftime("%Y.%m.%d"))
			self_path = os.path.dirname(os.path.realpath(__file__))
			creat_path(self_path + '/datas')
			print(u'任务已完成，Excel文件已保存至:%s'%self_path + '/' +save_path)
			w.save(self_path + '/' +save_path)


#根据系统获取raw_input中文编码结果
def gbk_encode(str):
	if os_is_windows:
		return str.decode('utf-8').encode('gbk')
	else:
		return str

#获取用户输入搜索城市
def get_citys():
	#citys = str(input(gbk_encode('请输入城市，多个城市使用#号隔开，输入Q退出程序: '))).decode(sys.stdin.encoding)
        citys = input('请输入城市，多个城市使用#号隔开，输入Q退出程序: ')
        return {'citys':citys}

def add_to_excel(ws,area,colData):
	cur_time = time.localtime(time.time())
	cur_mon_time = time.strftime('%Y/%m',cur_time)
	cur_for_mon_time = (datetime.date.today().replace(day=1)-datetime.timedelta(days=1)).strftime("%Y/%m")
	cur_day_time = time.strftime('%d',cur_time)
	index = 0
	title_col = colData[0]
	day_seg = 0
	if(len(colData) > 1) and cur_day_time in title_col:
		day_seg = title_col.index(cur_day_time)
	for col in colData:
		subIndex = 0
		for subCol in col:
			if len(colData) > 1 and index == 0 and len(subCol):
                                
				if (int(cur_day_time) >= int(subCol)) and (subIndex < day_seg + 1) or (int(subCol) > int(cur_day_time)):
					subCol = cur_for_mon_time + '/' + str(subCol)
				else:
					subCol = cur_mon_time + '/' + str(subCol)
			ws.write(subIndex,index,subCol)
			subIndex = subIndex+1
		index = index+1
def creat_path(path):
	is_exists=os.path.exists(path)
	if not is_exists:
		os.makedirs(path)
main()

