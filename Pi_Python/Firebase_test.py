import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase

firebase = firebase.FirebaseApplication("https://capstone2-1cd19-default-rtdb.firebaseio.com/", None)
result = firebase.get('device/first', None)
print (result)

cred = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'
})

dir = db.reference('device/first')
dir.update({'state' : 'on'})
