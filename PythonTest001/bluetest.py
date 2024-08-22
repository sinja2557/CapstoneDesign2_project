import bluetooth
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port=1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print("Accepted connection from ", address)
client_socket.send("Hello")

while 1:
    data = client_socket.recv(1024)
    print(data)
    
client_socket.close()