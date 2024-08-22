import os,sys

ADDWIFI001 = "sudo wpa_passphrase WIFINAME > wpa_supplicant.conf WIFIPW"
ADDWIFI002 = "sudo wpa_supplicant -B -i wlan0 -c wpa_supplicant.conf"

os.system(ADDWIFI001)
os.system(ADDWIFI002)