from machine import Pin
import time

in1 = Pin(2, Pin.OUT)  # IN1
in2 = Pin(3, Pin.OUT)  # IN2
stby = Pin(4, Pin.OUT) # STBY
stby.value(1)          # スタンバイ解除

def forward():
    in1.value(1)
    in2.value(0)

def reverse():
    in1.value(0)
    in2.value(1)

def brake():
    in1.value(1)
    in2.value(1)

def stop(): 
    in1.value(0)
    in2.value(0)

# テスト
stop()
time.sleep(1)
print("start")
while True:
    print("hello")
    forward()
    time.sleep(0.01)
    reverse()
    time.sleep(0.01)