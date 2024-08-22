import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase
import time

cred = credentials.Certificate('/home/pi/autodatabase.json')
firebase = firebase.FirebaseApplication("https://testod-3e067-default-rtdb.firebaseio.com/", None)
creda = credentials.Certificate('/home/pi/autodatabase.json')
firebase_admin.initialize_app(creda, {'databaseURL': 'https://testod-3e067-default-rtdb.firebaseio.com/'})


#==================== roll motor ==================
def stepA (newdata):
    change = newdata
    GPIO.setmode(GPIO.BOARD)
    ControlPin = [31,33,29,35]
    
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
            time.sleep(0.001)
    time.sleep(3)
        
    GPIO.cleanup()
    
    
def stepB (newdata):
    change = newdata
    GPIO.setmode(GPIO.BOARD)
    ControlPin = [31,33,29,35]
    
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
            time.sleep(0.001)
    time.sleep(3)
        
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
            stepA(128)
        elif checkdata < 0:
            checkdata += 1
            stepB(128)
            
    #=========firebase data insert|write========
    
    ref = db.reference('test001')
    ref.update({
            'olddata': newdata,
            })
    print('insert firebase data :')
    print(newdata)
    
    
    fp=open('/home/pi/olddata.txt','w')
    fp.write(newdata)
    fp.close()


#===================== main =======================




while True:
    
    result = firebase.get('test001/newdata', None)
    print('firebase data :')
    print(result)
    
    new=open('/home/pi/newdata.txt','r')
    newD = new.read(1)
    newdata=newD
    new.close()
    
    print('textfile data:')
    print(newdata)

    writenew = "%d"%result
    fp=open('/home/pi/newdata.txt','w')
    fp.write(writenew)
    fp.close()
    
    print('write newdata :')
    print(writenew)
    
    if writenew != newD:
        print('roll motor start')
        changedatas()
        
    
    print('overload prevent')
    time.sleep(5)
    
    

    
    

