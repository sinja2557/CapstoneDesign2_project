from bs4 import BeautifulSoup
from pprint import pprint
import re
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import RPi.GPIO as GPIO
import time
import bluetooth
import os, sys

def stepA (newdata):
    change = newdata
    GPIO.setmode(GPIO.BOARD)
    ControlPin = [29,33,31,35]
    
    for pin in ControlPin:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
        
    seq = [ [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
            [1,0,0,0],
            [1,0,0,1]]
    
    for i in range(change) :
        for halfstep in range(8):
            for pin in range (4):
                GPIO.output(ControlPin[pin], seq[halfstep] [pin])
            time.sleep(0.01)
    time.sleep(0.5)
        
    GPIO.cleanup()
    
    
def stepB (newdata):
    change = newdata
    GPIO.setmode(GPIO.BOARD)
    ControlPin = [29,33,31,35]
    
    for pin in ControlPin:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
        
    seq = [ [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]]
    
    for i in range(change) :
        for halfstep in range(8):
            for pin in range (4):
                GPIO.output(ControlPin[pin], seq[halfstep] [pin])
            time.sleep(0.01)
    time.sleep(0.5)
        
    GPIO.cleanup()
    
    
def changedatas ():
    new=open('/home/pi/newdata.txt','r')
    newD = new.read(1)
    old=open('/home/pi/olddata.txt','r')
    oldD = old.read(1)
    
    newdat=newD
    newdata=int(newD)
    olddata=int(oldD)
    checkdata = int(newD) - int(oldD)
    
    new.close()
    old.close()
    print(newdata)
    print(olddata)
    print(checkdata)
    
    
    
    # =========roll motor==========
    
    while checkdata != 0 :
        if checkdata >= 1:
            checkdata -= 1
            stepA(13)
        elif checkdata < 0:
            checkdata += 1
            stepB(13)
            
    #=========firebase data insert|write========
    
    ref = db.reference('device/ad002/manual')
    ref.update({
        'changedata': newdata,
        'nowdata': newD
        })
    print('insert firebase data :')
    print(newD)
    
    
    fp=open('/home/pi/olddata.txt','w')
    fp.write(newdat)
    fp.close()
    

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

print(find_current_weather)

check=0
if find_current_weather == "구름많음":
    print("구름많음")
    check=3
elif find_current_weather == "맑음":
    print("맑음")
    check=1
elif find_current_weather == "흐림":
    print("흐림")
    check=2
elif find_current_weather == "비":
    print("비")
    check=4
    
print(check)

    
print('write newdata :')
print(check)

new=open('/home/pi/newdata.txt','r')
newD = new.read(1)

new.close()

writenew = "%d"%check
fp=open('/home/pi/newdata.txt','w')
fp.write(writenew)
fp.close()

if writenew != newD:
    print('roll motor start')
    changedatas()

        
    
print('overload prevent')
time.sleep(5)


 