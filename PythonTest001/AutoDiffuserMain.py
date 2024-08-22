import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase
import time
import bluetooth
import os, sys

from bs4 import BeautifulSoup
from pprint import pprint
import re
import requests


import bluetooth
import os, sys
import time





cred = credentials.Certificate('/home/pi/firebase.json')
firebase = firebase.FirebaseApplication("https://capstone2-1cd19-default-rtdb.firebaseio.com/", None)
creda = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(creda,{'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'})

GPIO.setmode(GPIO.BOARD)

LED = 11
BUTT = 13

GPIO.setwarnings(False)

GPIO.setup(BUTT,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(LED,GPIO.OUT)




light = False

def mb(call):
    global light
    if light==False:
        GPIO.output(LED,1)
        blueon = "sudo sh /home/pi/blueon.sh"
        print("bluetooth on")
        os.system(blueon)
        
    else:
        GPIO.output(LED,0)
        btwifi = "sudo python3 /home/pi/bt_wifi.py"
        print("wifi")
        os.system(btwifi)
        
        
        
        
    light=not light






#==================== bluetooth button =================

#def bluebutton():
    

#==================== roll motor ==================
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

#==================== rasp data,firebase data change and roll ====================

def changedatas ():
    new=open('/home/pi/newdata.txt','r')
    newD = new.read(1)
    old=open('/home/pi/olddata.txt','r')
    oldD = old.read(1)
    
    newdata=newD
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
            stepB(13
                  
                  )
            
    #=========firebase data insert|write========
    
    ref = db.reference('device/ad002/manual') # change data@@@@@@@@@@@@@@@@@
    ref.update({
            'nowdata': newdata,
            })
    print('insert firebase data :')
    print(newdata)
    
    
    fp=open('/home/pi/olddata.txt','w')
    fp.write(newdata)
    fp.close()


#===================== manuel version =======================

def menualver():
    
    result = firebase.get('device/ad002/manual/changedata', None) #change data@@@@@@@@@@@@@@@@@@@@
    print('firebase data :')
    print(result)
    
    new=open('/home/pi/newdata.txt','r')
    newD = new.read(1)
    newdata=newD
    new.close()
    
    print('textfile data:')
    print(newD)

    writenew = '%d'%result
    fp=open('/home/pi/newdata.txt','w')
    fp.write(writenew)
    fp.close()
    
    print('write newdata :')
    print(result)
    
    if result != newD:
        print('roll motor start')
        changedatas()
    elif result == newD:
        print('same')
        
    
    print('overload prevent')
    time.sleep(0.5)


#=======================neopixel version =====================

def neopix():
    ledch = firebase.get('device/ad002/LED/onoff',None)
    print('neopixel check')
    print(ledch)
    if ledch == 0 :
        ledoff = 'sudo python3 /home/pi/neooff.py'
        os.system(ledoff)
    elif ledch == 1 :
        ledon = 'sudo python3 /home/pi/neoon.py'
        os.system(ledon)
    
    
def caseonoff():
    caseonoff = firebase.get('device/ad002/caseopen',None)
    new=open('/home/pi/case.txt','r')
    newD = new.read(3)
    new.close()
    
    print(newD)
    
    
    if caseonoff == 'off': #CLOSE CASE
        if caseonoff != newD:
            stepA(7)
            fp=open('/home/pi/case.txt','w')
            fp.write(caseonoff)
            fp.close()
        
    elif caseonoff == 'on': #OPEN CASE
        if caseonoff != newD:
            stepB(7)
            fp=open('/home/pi/case.txt','w')
            fp.write(caseonoff)
            fp.close()
            
            
        main()
            

def main():
    try:
        result = firebase.get('device/ad002/autocheck', None) #change data @@@@@@@@@@@@@@@@@@@@@@@@2
        print('auto check :')
        print(result)
         
        if result == 0:
            print('auto version')
            autover="sudo python3 /home/pi/weather_crawling_test.py"
            os.system(autover)
        elif result ==1:
            print('menual version')
            menualver()
        neopix()
        
        
    except:
        print('error')
        time.sleep(1)
    
        
    




#============================ main ==========================
GPIO.add_event_detect(BUTT,GPIO.RISING,callback=mb,bouncetime=300)
while True:
    caseonoff()
    