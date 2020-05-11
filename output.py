import RPi.GPIO as GPIO
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

def GPIO_demo(a):
    GPIO.output(5, a[2])
    GPIO.output(6, a[1])
    GPIO.output(13, a[0])

mode=[0, 0, 0]
GPIO_demo(mode)
mode=[0, 0, 1]
mode=[0, 1, 0]
mode=[0, 1, 1]
GPIO.cleanup()

os.system('sudo python playwav.py forbid_left_right.wav')
os.system('sudo python playwav.py forbid_long_stop.wav')
os.system('sudo python playwav.py forbid_park.wav')
os.system('sudo python playwav.py forbid_run.wav')
os.system('sudo python playwav.py forbid_straight.wav')
os.system('sudo python playwav.py forbid_straight_right.wav')
os.system('sudo python playwav.py forbid_turn_right.wav')
os.system('sudo python playwav.py forbid_whistle.wav')
os.system('sudo python playwav.py go_straight.wav')
os.system('sudo python playwav.py police_stop.wav')
os.system('sudo python playwav.py slow_down.wav')
os.system('sudo python playwav.py speed_limit40.wav')
os.system('sudo python playwav.py start.wav')
os.system('sudo python playwav.py stop_check.wav')
os.system('sudo python playwav.py turn_left.wav')
os.system('sudo python playwav.py turn_right.wav')
os.system('sudo python playwav.py forbid_turn_around.wav')