import bluetooth
import os, sys
import time

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port=1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print("Accepted connection from ", address)
client_socket.send("Hello")

while 1:
    print("SSID")
    wifi_ssid = ""
    client_socket.send("Input Wi-Fi SSID")
    data = client_socket.recv(1024)
    wifi_ssid = data.decode('utf-8')
    print(wifi_ssid)
    
    print("PWD")
    client_socket.send("Input Wi-Fi PWD")
    data = client_socket.recv(1024)
    wifi_pwd = data.decode('utf-8')
    print(wifi_pwd)
    break
    
dfile = "wpa_supplicant.conf"
if os.path.isfile(dfile):
    os.remove(dfile)
print("기존 파일 제거")

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

blueoff = "sudo sh /home/pi/blueoff.sh"
print("bluetooth off")
os.system(blueoff)

client_socket.close()
server_socket.close()
