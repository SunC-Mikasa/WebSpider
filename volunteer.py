import requests
from urllib.parse import urlencode

#Author: SunC-Mikasa

#Obtaining filtered activities held by Shenzhen Volunteer Union on v.sva.org.cn

#Set your age 
#Only capable of filtering according to minimum age requirement 
age = 16

#Set the district 
#福田区:2 罗湖区:3 南山区:4 盐田区:5 宝安区:6 龙岗区:7 光明新区:8 坪山区:9 龙华区:10 大鹏新区:11 其他:12 不限:None
DisID = 7

#Set the page amount you want (1 page = 20 activities) the program to go through
dl_page = 10
		
base_url = "http://v.sva.org.cn/default.aspx?"
ac_url = "http://v.sva.org.cn/default.aspx?_c=Program&_a=GetProfile&ProgramID="

headers = {
	'Host': 'v.sva.org.cn',
	'Referer': 'http://v.sva.org.cn/default.aspx?_c=ProgramSearch&_p=1&_ps=20&_sw1=active&DistrictID=7&lat=0&lng=0',
	'X-Request-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

ac_headers = {
	'Host': 'v.sva.org.cn',
	'X-Request-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def get_page(page):
	params = {
		'_c': 'ProgramSearch',
		'_a': 'GetPrograms',
		'_p': page,
		'_ps': '20',
		'_sw1': 'active',
		'DistrictID': DisID,
		'lat': '0',
		'lng': '0'
	}
	url = base_url + urlencode(params)
	print(url)
	response = requests.get(url, headers = headers)
	return response.json()
	
		
def parse_page(json):
	if json:
		items = json.get('Programs')
		for item in items:
			ac_link = ac_url + str(item.get('ProgramID'))
			print(ac_link)
			ac_r = requests.get(ac_link, headers = ac_headers)
			yield process_ac(ac_r.json())
		
			
def process_ac(ac_json):
	program = ac_json.get('Program')
	program_info = {}
	program_info['ServiceHour'] = program.get('ProgramServiceHours')
	program_info['Time'] = program.get('StartTime')[11:] + ' to ' + program.get('EndTime')[11:]
	program_info['Date'] = program.get('StartDate')[0:10] + ' to ' + program.get('EndDate')[0:10]
	program_info['ID'] = program.get('ProgramID')
	program_info['Name'] = program.get('ProgramName')
	if program.get('PositionsAvailable')>program.get('PositionsOccupied') and (program.get('RegGroupLimit')==0):
		if program.get('RegAgeMin'):
			if age<program.get('RegAgeMin'):
				return
			else:
				return program_info
				
		else:
			return program_info
	else:
		return

		
def write_txt(result):
	with open('result.txt','a',encoding='utf-8') as f:
		if result:
			for key in result: 
				if result[key]:
					if key=='ServiceHour':
						f.write(key+":"+str(result[key])+(5-len(str(result[key])))*' ')
					else:
						f.write(key+":"+str(result[key])+'  ')
				else:
					f.write(key+":"+'0'+'    ')
			f.write('\n')

				
if __name__ == '__main__':
	for page in range(1,dl_page+1):
		json = get_page(page)
		results = parse_page(json)
		for result in results: 
			write_txt(result)

	

		
	
	
