import os, sys
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'
})


ping = os.system("host www.google.com")
print(ping)

if(ping==0): #ping == 0 이면 네트워크 정상 작동
    dir = db.reference('device/first')
    dir.update({'state' : 'on'})
    print("Network connection success")
    





