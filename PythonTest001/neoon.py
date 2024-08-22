import board
import neopixel
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase
from bs4 import BeautifulSoup
from pprint import pprint
import re
import requests

cred = credentials.Certificate('/home/pi/firebase.json')
firebase = firebase.FirebaseApplication("https://capstone2-1cd19-default-rtdb.firebaseio.com/", None)
creda = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(creda,{'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'})

ledR = firebase.get('device/ad002/LED/R', None)
ledG = firebase.get('device/ad002/LED/G', None)
ledB = firebase.get('device/ad002/LED/B', None)#change data @@@@@@@@@@@@@@@@@@@@@@@@2


pixels = neopixel.NeoPixel(board.D18,30)
pixels.fill((ledR,ledG,ledB))
pixels.show()