import socket
if __name__ == '__main__':
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('localhost', 8001))
  sock.listen(5)
  sock.setblocking(0)
  connection,address = sock.accept()
  connection.settimeout(5)
  i=0
  while True:
    try:
      i=i+1
      print(i)
      buf = connection.recv(1024).decode()
      if buf == '1':
        connection.send('welcome to server!'.encode())
      else:
        connection.send('please go out!'.encode())
    except socket.timeout:
      print ('time out')
  connection.close()
