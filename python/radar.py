import RPi.GPIO as GPIO
import socketio
import time
import string
import threading
import json


Dist=[0]*200
Distmassage=[]

#超声波引脚定义
EchoPin = 0
TrigPin = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#初始化上下左右角度为90度
ServoLeftRightPos = 90
ServoUpDownPos = 90
g_frontServoPos = 90
g_nowfrontPos = 0

#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13
#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24 

#舵机引脚定义
FrontServoPin = 23
ServoUpDownPin = 9
ServoLeftRightPin = 11

#红外避障引脚定义 
AvoidSensorLeft = 12
AvoidSensorRight = 17

#蜂鸣器引脚定义
buzzer = 8

#循迹红外引脚定义
#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1  =  3   #定义左边第一个循迹红外传感器引脚为3口
TrackSensorLeftPin2  =  5   #定义左边第二个循迹红外传感器引脚为5口
TrackSensorRightPin1 =  4   #定义右边第一个循迹红外传感器引脚为4口
TrackSensorRightPin2 =  18  #定义右边第二个循迹红外传感器引脚为18口

#光敏电阻引脚定义
LdrSensorLeft = 7
LdrSensorRight = 6

#七彩灯RGB三色变量定义
red = 0
green = 0
blue = 0
#小车速度变量
CarSpeedControl = 80 



def init():
  global pwm_ENA
  global pwm_ENB
  global pwm_FrontServo
  global pwm_UpDownServo
  global pwm_LeftRightServo
  global pwm_rled
  global pwm_gled
  global pwm_bled

  GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
  GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
  GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
  GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
  GPIO.setup(buzzer,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(EchoPin,GPIO.IN)#超声波echo
  GPIO.setup(TrigPin,GPIO.OUT)#超声波Trig
  GPIO.setup(FrontServoPin, GPIO.OUT)#前舵机
  GPIO.setup(LED_R, GPIO.OUT)#rgb
  GPIO.setup(LED_G, GPIO.OUT)
  GPIO.setup(LED_B, GPIO.OUT)
  GPIO.setup(ServoUpDownPin, GPIO.OUT)
  GPIO.setup(ServoLeftRightPin, GPIO.OUT)
  GPIO.setup(AvoidSensorLeft,GPIO.IN)
  GPIO.setup(AvoidSensorRight,GPIO.IN)
  GPIO.setup(LdrSensorLeft,GPIO.IN)
  GPIO.setup(LdrSensorRight,GPIO.IN)
  GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
  GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
  GPIO.setup(TrackSensorRightPin1,GPIO.IN)
  GPIO.setup(TrackSensorRightPin2,GPIO.IN)
  #设置pwm引脚和频率为2000hz
  pwm_ENA = GPIO.PWM(ENA, 2000)
  pwm_ENB = GPIO.PWM(ENB, 2000)
  pwm_ENA.start(0)
  pwm_ENB.start(0)
  #设置舵机的频率和起始占空比
  pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
  pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
  pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
  pwm_FrontServo.start(0)
  pwm_UpDownServo.start(0)
  pwm_LeftRightServo.start(0)
  pwm_rled = GPIO.PWM(LED_R, 1000)
  pwm_gled = GPIO.PWM(LED_G, 1000)
  pwm_bled = GPIO.PWM(LED_B, 1000)
  pwm_rled.start(0)
  pwm_gled.start(0)
  pwm_bled.start(0)

  #小车前进	
def run():
  GPIO.output(IN1, GPIO.HIGH)
  GPIO.output(IN2, GPIO.LOW)
  GPIO.output(IN3, GPIO.HIGH)
  GPIO.output(IN4, GPIO.LOW)
  pwm_ENA.ChangeDutyCycle(CarSpeedControl)
  pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车后退
def back():
  GPIO.output(IN1, GPIO.LOW)
  GPIO.output(IN2, GPIO.HIGH)
  GPIO.output(IN3, GPIO.LOW)
  GPIO.output(IN4, GPIO.HIGH)
  pwm_ENA.ChangeDutyCycle(CarSpeedControl)
  pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车原地左转
def spin_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车原地右转
def spin_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#小车停止	
def brake():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)

def Distance(angle):
    t1=0
    t2=0
    while GPIO.input(EchoPin):
      pass
    time.sleep(0.004500)
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
      t1 = time.time()
    while GPIO.input(EchoPin) and time.time()-t1<0.02942:
      t2 = time.time()
    Dist[angle]=((t2 - t1)* 340 / 2) * 100

#摄像头舵机左右旋转到指定角度
def leftrightservo_appointed_detection(pos): 
  for i in range(1):   
    pwm_LeftRightServo.ChangeDutyCycle(2.5 + 10 * pos/180)
    time.sleep(0.02)							#等待20ms周期结束
    	#pwm_LeftRightServo.ChangeDutyCycle(0)	#归零信号

#摄像头舵机上下旋转到指定角度
def updownservo_appointed_detection(pos):  
  for i in range(1):  
    pwm_UpDownServo.ChangeDutyCycle(2.5 + 10 * pos/180)
    time.sleep(0.02)							#等待20ms周期结束
    	#pwm_UpDownServo.ChangeDutyCycle(0)	#归零信号

def frontservo_appointed_detection(pos):    
  pwm_FrontServo.ChangeDutyCycle(2.5 + 10 * pos/180)
  #time.sleep(0.025)


#巡线测试
def tracking_test():
    global infrared_track_value
    #检测到黑线时循迹模块相应的指示灯亮，端口电平为LOW
    #未检测到黑线时循迹模块相应的指示灯灭，端口电平为HIGH
    TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
    TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
    TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
    TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
    infrared_track_value_list = ['0','0','0','0']
    infrared_track_value_list[0] = str(1 ^TrackSensorLeftValue1)
    infrared_track_value_list[1] = str(1 ^TrackSensorLeftValue2)
    infrared_track_value_list[2] = str(1 ^TrackSensorRightValue1)
    infrared_track_value_list[3] = str(1 ^TrackSensorRightValue2)
    infrared_track_value = ''.join(infrared_track_value_list)
    

#避障红外引脚测试
def infrared_avoid_test():
    global infrared_avoid_value
    #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
    #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
    LeftSensorValue  = GPIO.input(AvoidSensorLeft)
    RightSensorValue = GPIO.input(AvoidSensorRight)
    infrared_avoid_value_list = ['0','0']
    infrared_avoid_value_list[0] = str(1 ^LeftSensorValue)
    infrared_avoid_value_list[1] = str(1 ^RightSensorValue)
    infrared_avoid_value = ''.join(infrared_avoid_value_list)
    	
#寻光引脚测试
def follow_light_test():
    global LDR_value
    #遇到光线,寻光模块的指示灯灭,端口电平为HIGH
    #未遇光线,寻光模块的指示灯亮,端口电平为LOW
    LdrSersorLeftValue  = GPIO.input(LdrSensorLeft)
    LdrSersorRightValue = GPIO.input(LdrSensorRight)  
    LDR_value_list = ['0','0']
    LDR_value_list[0] = str(LdrSersorLeftValue)
    LDR_value_list[1] = str(LdrSersorRightValue)	
    LDR_value = ''.join(LDR_value_list)

    #小车鸣笛
def whistle():
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.001)	
	
#七彩灯亮指定颜色
def color_led_pwm(iRed,iGreen, iBlue):
    v_red = (100*iRed)/255
    v_green = (100*iGreen)/255
    v_blue = (100*iBlue)/255
    pwm_rled.ChangeDutyCycle(v_red)
    pwm_gled.ChangeDutyCycle(v_green)
    pwm_bled.ChangeDutyCycle(v_blue)
    time.sleep(0.02)


#socketio通信
sio = socketio.Client()
ut = "1"

@sio.event
def connect():
    print('connection established')

# listen server
@sio.on('control_massage')
def control_message(data):
    print('user_message received with ', data)

@sio.event
def disconnect():
    print('disconnected from server')


def radar():
   while True:
    for i in range(0,180,2):
      thread1 = threading.Thread(target = Distance,args=(i))
      thread1.start()
      thread1.join()
      frontservo_appointed_detection(i)
      time.sleep(0.025)
      print(i,int(Dist[i]))
      Distmassage.append({i:int(Dist[i])})
      if(i%20==18):
        sio.emit('radar',json.dumps(Distmassage),namespace="/")
        Distmassage.clear()
    for i in range(180,0,-2):
      thread1 = threading.Thread(target = Distance,args=(i))
      thread1.start()
      thread1.join()
      frontservo_appointed_detection(i)
      time.sleep(0.025)
      print(i,int(Dist[i]))
      Distmassage.append({i:int(Dist[i])})
      if(i%20==2):
        sio.emit('radar',json.dumps(Distmassage),namespace="/")
        Distmassage.clear()

if __name__ == '__main__':
  init()
  sio.connect('http://192.168.0.107:7001',namespaces=["/","/car"])
  thread1 = threading.Thread(target = radar)
  thread1.start()
  