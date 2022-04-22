import socket

s = socket.socket()
s.bind(("",9999))
s.listen(1) # Accepts up to 10 connections.

buf_size = 1024

while True:
    sc, address = s.accept()
    print(address)
    f = open("output.txt",'wb') #open in binary
    count = 0
    while (True):
        chunk = sc.recv(buf_size)
        print("data recv: ", len(chunk))
        count += len(chunk)
        f.write(chunk)
        if len(chunk) < buf_size:
            break
    print("received {} bytes".format(count))
    f.close()
    sc.close()

s.close()