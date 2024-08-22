from bs4 import BeautifulSoup
from pprint import pprint
import re
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'
})

html = requests.get('https://search.naver.com/search.naver?query=날씨')
#pprint(html.text)

soup = BeautifulSoup(html.text, 'html.parser')

data1 = soup.find('div', {'class': 'main_pack'})

find_current_address = data1.find('h2', {'class': 'title'}).text
print("현재 위치 : " + find_current_address)

find_current_weather = data1.find('div', {'class': 'weather_main'}).text.split(' ')[1]
print("현재 날씨 : " + find_current_weather)

find_current_temp = data1.find('div',{'class': 'temperature_text'}).text
find_current_temp = re.findall('\d+', find_current_temp)
print("현재 기온 : " + find_current_temp[0] + '°')

data2 = data1.find('dl',{'class': 'summary_list'}).text
#print(data2)

find_current_humidity = re.findall('\d+', data2)
#print(find_current_humidity)
print("현재 습도 : " + find_current_humidity[2] + "%")

find_current_dust = data1.find('li', {'class': 'item_today'}).text.split()
print(find_current_dust[0] + ' : ' + find_current_dust[1])

#Firebase Update
dir = db.reference('device/first/weather')
dir.update({'location' : find_current_address})
dir.update({'info' : find_current_weather})
dir.update({'temp' : find_current_temp[0]})
dir.update({'humidity' : find_current_humidity[2]})
dir.update({'dust' : find_current_dust[1]})
