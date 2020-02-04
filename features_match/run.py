import cv2 as cv
#import RPi.GPIO as GPIO
from os import system
import time
#version 1.5
#计划改进：效率方面，事先计算库中的特征点数据，为树莓派的运算节省时间
#交通标志牌识别，模板库中共有6个交通标志
#识别测试样例不包含极端特殊拍摄角度




#def fun(arg):
    #GPIO.cleanup()
    #print(arg)
    #system('sudo halt')
    #print('success')
    

#def GPIO_demo():
    #GPIO.output(5, state[3])
    #GPIO.output(6, state[2])
    #GPIO.output(13, state[1])
    #GPIO.output(19, state[0])

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(5, GPIO.OUT)
#GPIO.setup(6, GPIO.OUT)
#GPIO.setup(13, GPIO.OUT)
#GPIO.setup(19, GPIO.OUT)
#GPIO.setup(26, GPIO.OUT)
#GPIO.output(26,1)
state=[0,0,0,0]

#GPIO_demo()
mark_description = ['go straight', 'whistle', 'turn left', 'turn right', 'move right', 'move left']
capture = cv.VideoCapture(0)
orb = cv.ORB_create()
#创建BF暴力匹配器，用于捕捉到的图和模板进行特征点匹配
bf = cv.BFMatcher(cv.NORM_HAMMING)

while True:
    t1 = cv.getTickCount()  # 运行时间计算
    #ret, frame = capture.read()
    #cv.imshow("video", frame)
    #c = cv.waitKey(20)
        
    #if c == ord('q'):
        #break
    
    #img_captured = frame
    img_captured = cv.imread('D:\\picbase\\test\\13.jpg')
    #ORB算法检测特征点
    kp_captured, des_captured = orb.detectAndCompute(img_captured, None)

    most_match_number = 0
    best_picnum = None

    #在模板库中寻找特征点匹配程度最高的图片
    for picnum_base in range(1, 7):
        read_path_base = "D:\\picbase\\mark_base\\" + str(picnum_base) + ".jpg"
        img1 = cv.imread(read_path_base)
        kp1, des1 = orb.detectAndCompute(img1, None)
        #使用k-最近邻匹配方式
        matches = bf.knnMatch(des1, des_captured, k = 2)

        good_match = [ ]
        for m, n in matches:
            if m.distance < 0.7*n.distance:
                good_match.append(m)

        if len(good_match) > most_match_number:
            best_picnum = picnum_base
            most_match_number = len(good_match)

        print("{:8d}".format(picnum_base), ":{:8d}".format(len(good_match)))
    if most_match_number >= 5:
        print("result:{}".format(mark_description[best_picnum - 1]))
        if best_picnum==3:
            state=[0,0,1,0]
            #GPIO_demo()
    else:
        state = [0,0,0,0]
        #GPIO_demo()
    t2 = cv.getTickCount()  # 运行时间计算
    print("state:", state)
    print("running time:", (t2 - t1) * 1000 / cv.getTickFrequency(), "ms")  # 给出运行时间
    #guanjichengxu

#GPIO.setmode(GPIO.BCM)
#GPIO_PIN=4
#GPIO.setup(GPIO_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(GPIO_PIN,GPIO.FALLING,bouncetime=2000,callback=fun)
cv.destroyAllWindows()

