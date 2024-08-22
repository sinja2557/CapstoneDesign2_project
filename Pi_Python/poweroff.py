import os, sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'
})

diffuser_name = "first"

dir = db.reference('device/'+diffuser_name)
dir.update({'state' : 'off'})
print("power off")