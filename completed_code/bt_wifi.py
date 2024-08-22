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

default_name = '/home/pi/device_name.txt' #기기 고유명 txt 파일

if os.path.isfile(default_name):
    print("Device_name existed.\n")
    f = open(default_name, 'r+')
    f.seek(0)
    device_name = f.read()
    print(device_name)
    f.close()
    
else:
    print("Device_name not existed.\n")
    f = open(default_name, 'w+')
    f.seek(0)
    f.write('first') #기기 고유명 설정 (first , second ...)
    f.seek(0)
    device_name = f.read()
    print(device_name)
    f.close()

class ping_timeout(Exception): # ping 예외처리
    def __init__(self, msg='error occured!'):
        self.msg = msg
        
    def __str__(self):
        return self.msg
               
network_service = 'sudo service networking restart'
ifconfig_down = "sudo ifconfig wlan0 down"
ifconfig_up = "sudo ifconfig wlan0 up"

if os.path.isfile(dfile):
    
    print("Wifi info value existed.\n")
    
    try:
        wifi02 = "sudo wpa_supplicant -B -i wlan0 -c wpa_supplicant.conf"
        os.system(wifi02)

        os.system(network_service)
        os.system(ifconfig_down)
        os.system(ifconfig_up)
        
        time.sleep(15) #네트워크 연결을 위한 시간
        ping = os.system("host www.google.com")
        
        if(ping==0):
        
            dir = db.reference('device/'+ device_name)
            dir.update({'state' : 'on'})
            print("Network connection success\n")
        
            blueoff = "sudo sh /home/pi/blueoff.sh"
            print("bluetooth off\n")
            os.system(blueoff)
            
            exit
            
        elif(ping!=0):
            raise ping_timeout("Ping is Timeout.")
            
    except ping_timeout:
        os.remove(dfile)
        print("기존 파일 제거")
        
        time.sleep(1)
        
        re_bt_wifi = "sudo python3 /home/pi/bt_wifi.py"
        os.system(re_bt_wifi)
        
        exit
        
else:
    print("Wifi info value not existed.")
    
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port=1
    server_socket.bind(("",port))
    server_socket.listen(1)

    client_socket,address = server_socket.accept()
    print("Accepted connection from ", address)
    client_socket.send("Input your Wi-Fi SSID + PWD")

    while 1:
        print("SSID + PWD\n")
        wifi_value = ""
        data = client_socket.recv(1024)
        wifi_value = data.decode('utf-8')
        print(wifi_value)
        wifi_ssid = wifi_value.split(' ')[0]
        wifi_pwd = wifi_value.split(' ')[1]
        
        break
        
    try:
        wifi01 = "sudo wpa_passphrase " + wifi_ssid + ' ' + wifi_pwd + " > wpa_supplicant.conf"
        wifi02 = "sudo wpa_supplicant -B -i wlan0 -c wpa_supplicant.conf"
        print("Wifi SSID & PWD")

        os.system(wifi01)
        os.system(wifi02)

        os.system(network_service)
        os.system(ifconfig_down)
        os.system(ifconfig_up)
    
        time.sleep(15) #네트워크 연결을 위한 시간
    
        ping_test = "host www.google.com"
        ping = os.system(ping_test)
            
        if(ping==0):
            dir = db.reference('device/'+ device_name)
            dir.update({'state' : 'on'})
            print("Network connection success\n")
            
            client_socket.send(device_name) #앱에 고유명 전달
            time.sleep(1)
            
            blueoff = "sudo sh /home/pi/blueoff.sh"
            print("bluetooth off\n")
            os.system(blueoff)
                
            print("socket closing\n")
            client_socket.close()
            server_socket.close()
            time.sleep(1)
                
            exit
                
        elif(ping!=0):
            raise ping_timeout("Ping is Timeout.")
            
    except ping_timeout:
        os.remove(dfile)
        print("기존 파일 제거\n")
        
        client_socket.send("Failed, Please reconnect.")
        time.sleep(1)
        
        client_socket.close()
        server_socket.close()
            
        re_bt_wifi = "sudo python3 /home/pi/bt_wifi.py"
        os.system(re_bt_wifi)
        
        exit
            