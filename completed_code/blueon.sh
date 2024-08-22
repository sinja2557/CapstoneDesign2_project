sudo bluetoothctl <<EOF
power on
discoverable on
pairable on
EOF

hciconfig hci0 sspmode 0
#sudo bt-agent -c NoInputNoOutput -p /root/bluetooth.cfg &
