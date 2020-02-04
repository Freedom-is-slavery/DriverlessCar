from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import PIL.Image as Image
import time
import cv2
import os
import RPi.GPIO as GPIO


def GPIO_demo(a):
    GPIO.output(5, a[2])
    GPIO.output(6, a[1])
    GPIO.output(13, a[0])


def move(index_number):
    if index_number == 0:
        os.system('sudo python playwav.py forbid_left_right.wav')
    elif index_number == 1:
        os.system('sudo python playwav.py forbid_long_stop.wav')
    elif index_number == 2:
        os.system('sudo python playwav.py forbid_park.wav')
    elif index_number == 3:
        os.system('sudo python playwav.py forbid_run.wav')
    elif index_number == 4:
        os.system('sudo python playwav.py forbid_straight.wav')
    elif index_number == 5:
        os.system('sudo python playwav.py forbid_straight_right.wav')
    elif index_number == 6:
        os.system('sudo python playwav.py forbid_turn_around.wav')
    elif index_number == 7:
        os.system('sudo python playwav.py forbid_turn_right.wav')
    elif index_number == 8:
        os.system('sudo python playwav.py forbid_whistle.wav')
    elif index_number == 9:
        GPIO_demo([0, 0, 1])
        os.system('sudo python playwav.py go_straight.wav')
    elif index_number == 10:
        GPIO_demo([0, 0, 1])
        os.system('sudo python playwav.py go_straight.wav')
    elif index_number == 11:
        GPIO_demo([1, 0, 0])
        os.system('sudo python playwav.py slow_down.wav')
    elif index_number == 12:
        os.system('sudo python playwav.py police_stop.wav')
    elif index_number == 13:
        GPIO_demo([0, 1, 0])
        os.system('sudo python playwav.py turn_left.wav')
    elif index_number == 14:
        GPIO_demo([0, 1, 1])
        os.system('sudo python playwav.py turn_right.wav')
    elif index_number == 15:
        os.system('sudo python playwav.py speed_limit40.wav')
    elif index_number == 16:
        os.system('sudo python playwav.py stop_check.wav')
    elif index_number == 17:
        GPIO_demo([0, 1, 0])
        os.system('sudo python playwav.py turn_left.wav')
    elif index_number == 18:
        GPIO_demo([0, 1, 1])
        os.system('sudo python playwav.py turn_right.wav')

    time.sleep(0.2)
    GPIO_demo([0, 0, 0])

def recognition(model_dir, classes):
    #clicked = False

    #def onMouse(event, x, y, flags, param):
        #global clicked
        #if event == cv2.EVENT_LBUTTONUP:
            #clicked = True

    cameraCapture = cv2.VideoCapture(0)
    cameraCapture.set(3, 320)  # 帧宽度
    cameraCapture.set(4, 240)  # 帧高度

    success, frame = cameraCapture.read()
    print("Read back:", success)

    saver = tf.train.import_meta_graph(model_dir + ".meta")
    with tf.Session() as sess:
        saver.restore(sess, model_dir)
        x = tf.get_default_graph().get_tensor_by_name("images:0")
        keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")
        y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")


        while success and cv2.waitKey(1) == -1:
            time1 = time.time()
            cv2.imshow('MyWindow', frame)
            success, frame = cameraCapture.read()
            img = Image.fromarray(frame)

            #图像预处理，将图片转化成灰度并缩小尺寸
            img = np.array(img.convert('L').resize((128, 128)), dtype=np.float32)
            img = img.reshape((1, 128 * 128))
            img = img / 255.0

            prediction = sess.run(y, feed_dict={x: img, keep_prob: 1.0})

            index = np.argmax(prediction)
            probability = prediction[0][index]

            # 设置probability为0.8是为了提高识别稳定性
            if probability > 0.8:
                move(index)

            time2 = time.time()
            print(classes[index])
            print('using time: ', time2 - time1)

            print('probability: %.3g' % probability)

            #参数选择，延迟进行下一轮识别的秒数
            time.sleep(5)

        cv2.destroyWindow('MyWindow')
        cameraCapture.release()


if __name__ == "__main__":


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # 这里是各种标志和交警手势的分类，可添加和更改
    classes = ['forbid_run', 'forbid_straight',
               'forbid_turn_around', 'forbid_turn_right', 'forbid_whistle',
               'go straight', 'police_go_straight', 'police_slow_down',
               'police_stop', 'police_turn_left', 'police_turn_right',
               'speed_limit40', 'turn_left', 'turn_right']

    model_dir = "model/model.ckpt"
    recognition(model_dir, classes)

