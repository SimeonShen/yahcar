# websocket协议通信
import threading
import time
import websocket
 
def when_message(ws, message):
    print('接收到的消息：' + message)
 
 
# 当建立连接后，死循环不断输入消息发送给服务器
# 这里需要另起一个线程
def when_open(ws):
    def run():
        while True:
            a = input('发送服务端：')
            ws.send(a)
            time.sleep(0.5)
            if a == 'close':
                ws.close()
                break
 
    t = threading.Thread(target=run)
    # t.setDaemon(True)
    t.start()
 
def when_close(ws):
    print('连接关闭')
 
if __name__ == '__main__':
    ws = websocket.WebSocketApp('http://localhost:7001/', on_message=when_message, on_open=when_open, on_close=when_close)
    ws.run_forever()
