import bluetooth
import os, sys
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/firebase.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://capstone2-1cd19-default-rtdb.firebaseio.com/'
})

dfile = "wpa_supplicant.conf"

if os.path.isfile(dfile):
    
    print("1")
    
    wifi02 = "sudo wpa_supplicant -B -i wlan0 -c wpa_supplicant.conf"
    os.system(wifi02)
    
    wlan0_down = "sudo ifconfig wlan0 down"
    wlan0_up = "sudo ifconfig wlan0 up"

    os.system(wlan0_down)
    print("down\n")
    time.sleep(5)
    os.system(wlan0_up)
    print("up\n")
    
    time.sleep(15) #네트워크 연결을 위한 시간
    ping = os.system("host www.google.com")
    if(ping==0):
        
        dir = db.reference('device/first')
        dir.update({'state' : 'on'})
        print("Network connection success")
        
        blueoff = "sudo sh /home/pi/blueoff.sh"
        print("bluetooth off")
        os.system(blueoff)

        exit
        
    elif(ping!=0):
        
        os.remove(dfile)
        print("기존 파일 제거")
        os.system("sudo /home/pi/bt_wifi_updating.py")
        
        exit
        
else:
    print("2")
    
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port=1
    server_socket.bind(("",port))
    server_socket.listen(1)

    client_socket,address = server_socket.accept()
    print("Accepted connection from ", address)
    client_socket.send("Input your Wi-Fi SSID + PWD")

    while 1:
        print("SSID + PWD")
        wifi_value = ""
        data = client_socket.recv(1024)
        wifi_value = data.decode('utf-8')
        print(wifi_value)
        wifi_ssid = wifi_value.split(' ')[0]
        wifi_pwd = wifi_value.split(' ')[1]
        
        break

    wifi01 = "sudo wpa_passphrase " + wifi_ssid + ' ' + wifi_pwd + " > wpa_supplicant.conf"
    wifi02 = "sudo wpa_supplicant -B -i wlan0 -c wpa_supplicant.conf"
    print("Wifi SSID & PWD")

    os.system(wifi01)
    os.system(wifi02)

    wlan0_down = "sudo ifconfig wlan0 down"
    wlan0_up = "sudo ifconfig wlan0 up"

    os.system(wlan0_down)
    print("down\n")
    time.sleep(5)
    os.system(wlan0_up)
    print("up\n")
    
    time.sleep(15) #네트워크 연결을 위한 시간
    
    ping = os.system("host www.google.com")
    if(ping==0):
        dir = db.reference('device/first')
        dir.update({'state' : 'on'})
        print("Network connection success")
        
    elif(ping!=0):
        os.remove(dfile)
        print("기존 파일 제거")
        os.system("sudo /home/pi/bt_wifi.py")

    blueoff = "sudo sh /home/pi/blueoff.sh"
    print("bluetooth off")
    os.system(blueoff)

    print("socket closing")
    client_socket.close()
    server_socket.close()


