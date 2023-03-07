import socketio

sio = socketio.Client()
ut = "1"


@sio.event
def connect():
    print('connection established')


# 监听服务端推送消息
@sio.on('CustomVisited')
def user_message(data):
    print('user_message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


# 连接服务端 IP+端口
sio.connect('http://192.168.0.100:7001',namespaces="/car")
print("000")

# 向服务端发送消息
sio.emit('sub_user_message',ut,namespace="/car")
sio.wait()