import os, sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'
})

default_name = '/home/pi/device_name.txt' #기기 고유명 txt 파일

if os.path.isfile(default_name):
    print("Device_name existed.\n")
    f = open(default_name, 'r+')
    f.seek(0)
    device_name = f.read()
    print(device_name)
    f.close()

dir = db.reference('device/' + device_name)
dir.update({'state' : 'off'})