import socket

HOST = input("esp32 ip>> ")
PORT = 4545

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'con')
data = s.recv(1024).decode('utf-8')
print(data)

while True:
    dt = input("esp32>> ")
    if dt == "exit":
        break
    s.sendall(dt.encode('utf-8'))  
    response = s.recv(1024).decode('utf-8')
    print(response)

s.close()
