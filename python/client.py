import time
import socket
if __name__ == '__main__':
  i=0
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(('localhost', 7001))
  sock.setblocking(0)
  while True:
    time.sleep(10)
    i=i+1
    try:
      sock.send('1'.encode())
      print(i)
      print (sock.recv(1024).decode())
    except:
      print('error!')
  sock.close()