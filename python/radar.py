import RPi.GPIO as GPIO
import socket
import time
import string
import threading

FrontServoPin = 23

#超声波引脚定义
EchoPin = 0
TrigPin = 1

def init():
    global pwm_ENA
    global pwm_ENB
    global pwm_FrontServo
    global pwm_UpDownServo
    global pwm_LeftRightServo
    global pwm_rled
    global pwm_gled
    global pwm_bled

    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    GPIO.setup(FrontServoPin, GPIO.OUT)

    #设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    #设置舵机的频率和起始占空比
    pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
    pwm_FrontServo.start(0)

    #超声波测距函数
def Distance_test():
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
        t1 = time.time()
    while GPIO.input(EchoPin):
        pass
        t2 = time.time()
    time.sleep(0.000015)
    return ((t2 - t1)* 340 / 2) * 100

def frontservo_appointed_detection(pos): 
    for i in range(18):   
    	pwm_FrontServo.ChangeDutyCycle(2.5 + 10 * pos/180)
    	time.sleep(0.0001)

if __name__ == '__main__':
  for i in range(180):
    frontservo_appointed_detection(i)
    Dist=Distance_test()
    print(i+":"+Dist)