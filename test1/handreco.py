# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test3.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import math
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 278)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 160, 121, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, -40, 721, 581))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-image: url(/home/pi/Desktop/shoushi/jiemianbeijing.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 160, 111, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(140, 30, 351, 111))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.label.raise_()
        self.pushButton_2.raise_()
        self.pushButton.raise_()
        self.textEdit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 624, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(self.slot1)
        self.pushButton.clicked.connect(self.slot2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "开始"))
        self.pushButton.setText(_translate("MainWindow", "处理"))

    def slot1(self, MainWindow):
        camera = PiCamera()
        camera.resolution = (540, 540)
        camera.awb_mode = 'fluorescent'
        camera.image_effect = 'none'
        # rawCapture = PiRGBArray(camera, size=(480, 480))
        camera.start_preview()
        sleep(3)
        for i in range(0, 60, 1):
            sleep(0.25)
            camera.capture('/home/pi/Desktop/shoushi/zhaopian/PAIZHAO%s.jpg' % i)
        camera.stop_preview()
        #self.textEdit.insertPlainText("jjjjj ")

    def slot2(self, MainWindow):
        N = 60

        x_ = [3] * N
        y_ = [3] * N
        HY = [3] * N
        ###############################################
        # 开始读取照片，YCrCb寻找手的位置
        for h in range(0, N, 1):
            imge = cv2.imread('/home/pi/Desktop/shoushi/zhaopian/PAIZHAO%s.jpg' % (h))
            row = imge.shape[0]
            col = imge.shape[1]
            img1 = cv2.resize(imge, (int(col / 4), int(row / 4)))
            rows, cols, channels = img1.shape
            imgYcc = cv2.cvtColor(img1, cv2.COLOR_BGR2YCR_CB)
            img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            imgSkin = np.zeros(img.shape, np.uint8)
            imgSkin = img.copy()
            for r in range(rows):
                for c in range(cols):
                    skin = 0
                    R = img.item(r, c, 0)
                    G = img.item(r, c, 1)
                    B = img.item(r, c, 2)
                    Y = imgYcc.item(r, c, 0)
                    Cr = imgYcc.item(r, c, 1)
                    Cb = imgYcc.item(r, c, 2)
                    if R > G and R > B:
                        if (G >= B and 5 * R - 12 * G + 7 * B + 100 >= 0) or (G < B and 5 * R + 7 * G - 12 * B >= 0):
                            if Cr > 135 and Cr < 180 and Cb > 85 and Cb < 135 and Y > 80:
                                skin = 1
                    if 0 == skin:
                        imgSkin.itemset((r, c, 0), 0)
                        imgSkin.itemset((r, c, 1), 0)
                        imgSkin.itemset((r, c, 2), 0)
            imgSkin = cv2.cvtColor(imgSkin, cv2.COLOR_BGR2GRAY)
            ret1, th1 = cv2.threshold(imgSkin, 55, 255, cv2.THRESH_BINARY)
            kernel = np.ones((2, 2), np.uint8)
            closing = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
            # cv2.imshow('closing',imgSkin)
            (_, cnts, _) = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cnts == []:
                num[h] = num[h - 1]
                x_[h] = x_[h - 1]
                y_[h] = y_[h - 1]
                continue
            if len(cnts) == 1:
                num[h] = num[h - 1]
                x_[h] = x_[h - 1]
                y_[h] = y_[h - 1]
                continue
            c = sorted(cnts, key=cv2.contourArea, reverse=True)[1]  # 找到第二大的轮廓
            rect = cv2.minAreaRect(c)
            box = np.int0(cv2.boxPoints(rect))
            Xs = [i[0] for i in box]
            Ys = [i[1] for i in box]
            x1 = 4 * min(Xs)
            x2 = 4 * max(Xs)
            y1 = 4 * min(Ys)
            y2 = 4 * max(Ys)
            height = y2 - y1
            width = x2 - x1
            x0 = int((x2 + x1) / 2)
            y0 = int((y2 + y1) / 2)
            # print((x0, y0))
            x_[h] = x0
            y_[h] = y0
            # print(y1,y2,x1,x2)
            cropImg = imge[max(y1 - 40, 0):y1 + height + 60, max(x1 - 40, 0):x1 + width + 30]
            ########################################################
            # RGB空间提取手的轮廓
            img = cropImg
            rows, cols, channels = img.shape
            imgSkin = np.zeros(img.shape, np.uint8)
            imgSkin = img.copy()
            for r in range(rows):
                for c in range(cols):
                    B = img.item(r, c, 0)
                    G = img.item(r, c, 1)
                    R = img.item(r, c, 2)
                    skin = 0
                    if (abs(R - G) > 10) and (R + 5 > G) and (R + 5 > B):
                        if (R > 95) and (G > 40) and (B > 20) and (max(R, G, B) - min(R, G, B) > 15):
                            skin = 1
                    elif (abs(R - G) <= 20) and (R + 5 > G) and (R + 5 > B):
                        if (R > 210) and (G > 200) and (B > 160):
                            skin = 1
                    if 0 == skin:
                        imgSkin.itemset((r, c, 0), 0)
                        imgSkin.itemset((r, c, 1), 0)
                        imgSkin.itemset((r, c, 2), 0)
            imgSkin = cv2.cvtColor(imgSkin, cv2.COLOR_BGR2GRAY)
            ret1, th1 = cv2.threshold(imgSkin, 35, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5, 5), np.uint8)
            closing = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
            (_, cnts, _) = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cnts == []:
                num[h] = num[h - 1]
                x_[h] = x_[h - 1]
                y_[h] = y_[h - 1]
                continue
            c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]  # 找到第一大的轮廓
            rect = cv2.minAreaRect(c)
            box = np.int0(cv2.boxPoints(rect))
            Xs = [i[0] for i in box]
            Ys = [i[1] for i in box]
            x1 = min(Xs)
            x2 = max(Xs)
            y1 = min(Ys)
            y2 = max(Ys)
            Y1 = max(y1 - 5, 0)
            Y2 = min(y2 + 5, img.shape[0])
            X1 = max(x1 - 5, 0)
            X2 = min(x2 + 5, img.shape[1])
            cropImg = img[Y1:Y2, X1:X2]
            #################################################################################
            # 生成黑白照片
            rows, cols, channels = cropImg.shape
            for r in range(rows):
                for c in range(cols):
                    B = cropImg.item(r, c, 0)
                    G = cropImg.item(r, c, 1)
                    R = cropImg.item(r, c, 2)
                    skin = 0
                    if (abs(R - G) > 10) and (R + 5 > G) and (R + 5 > B):
                        if (R > 95) and (G > 40) and (B > 20) and (max(R, G, B) - min(R, G, B) > 15):
                            skin = 1
                    elif (abs(R - G) <= 20) and (R + 5 > G) and (R + 5 > B):
                        if (R > 210) and (G > 200) and (B > 160):
                            skin = 1

                    if 0 == skin:
                        cropImg.itemset((r, c, 0), 0)
                        cropImg.itemset((r, c, 1), 0)
                        cropImg.itemset((r, c, 2), 0)
                    else:
                        cropImg.itemset((r, c, 0), 255)
                        cropImg.itemset((r, c, 1), 255)
                        cropImg.itemset((r, c, 2), 255)
            # cv2.imwrite('test.jpg', cropImg)
            ############################################
            img = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
            # img = cv2.imread('test.jpg', 0)
            # img=cropImg
            (kuan, chang) = img.shape
            # kuan = int(kuan)
            # chang = int(chang)
            # 高斯模糊
            imga = cv2.GaussianBlur(img, (9, 9), 0)
            # 二值化处理
            ret, thresh1 = cv2.threshold(imga, 127, 255, cv2.THRESH_BINARY)  # 深色背景下的二值化
            # ret, thresh2 = cv2.threshold(imga, 127, 255, cv2.THRESH_BINARY_INV)  # 浅色背景下的二值化
            # mask=imga
            mask = thresh1  # 深色背景改为1，浅色背景改为2，颜色捕捉改为mask2
            # 获取手掌心，(x,y)为手掌圆圆心，maxdist为半径
            distance = cv2.distanceTransform(mask, cv2.DIST_L2, 5, cv2.CV_32F)
            maxdist = 0
            for i in range(distance.shape[0]):
                for j in range(distance.shape[1]):
                    dist = distance[i][j]
                    if maxdist < dist:
                        x = j
                        y = i
                        maxdist = dist
            cv2.circle(img, (x, y), maxdist, (255, 100, 255), 1, 8, 0)
            # cv2.imshow('x',mask)
            # print(maxdist)
            # 获取轮廓,以字典的形式存在contours中
            image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # 冒泡排序找到最大的轮廓
            m = len(contours)
            j = 0
            lenj = len(contours[0])
            for i in range(0, m, 1):
                Li = len(contours[i])
                if Li > lenj:
                    j = i
                    lenj = Li
            # cv2.imshow('2',img)
            # print(contours[j])
            # 计算距离
            [(a, b)] = contours[j][0]
            cv2.line(img, (a, b), (x, y), 1)
            L1 = math.sqrt((a - x) ** 2 + (b - y) ** 2)
            L = len(contours[j]) - 3
            lenth = [0] * L
            dian = [0] * L
            lenth[0] = L1
            dian[0] = (a, b)
            ix = 1
            for i in range(3, L, 1):
                [(a, b)] = contours[j][i]
                len0 = math.sqrt((a - x) ** 2 + (b - y) ** 2)
                [(a1, b1)] = contours[j][i + 1]
                len1 = math.sqrt((a1 - x) ** 2 + (b1 - y) ** 2)
                [(a2, b2)] = contours[j][i + 2]
                len2 = math.sqrt((a2 - x) ** 2 + (b2 - y) ** 2)
                [(a3, b3)] = contours[j][i - 1]
                len3 = math.sqrt((a3 - x) ** 2 + (b3 - y) ** 2)
                [(a4, b4)] = contours[j][i - 2]
                len4 = math.sqrt((a4 - x) ** 2 + (b4 - y) ** 2)
                [(a5, b5)] = contours[j][i - 3]
                len5 = math.sqrt((a5 - x) ** 2 + (b5 - y) ** 2)
                [(a6, b6)] = contours[j][i + 3]
                len6 = math.sqrt((a6 - x) ** 2 + (b6 - y) ** 2)
                if len0 > len1 and len0 > len3:  # and len0 > len3 and len0 > len4:  # and len0>len5 and len0>len6:
                    lenth[ix] = len0
                    dian[ix] = (a, b)
                    ix = ix + 1
            # 处理数组
            lx = len(dian)
            for i in range(lx - 1, -1, -1):
                if dian[i] == 0 or abs(lenth[i] - maxdist) < (maxdist):
                    del dian[i]
                    del lenth[i]
            lx = len(dian)
            for i in range(len(dian) - 1, -1, -1):
                (x_0, y_0) = dian[i]
                if x_0 == 0 or x_0 == chang - 1 or y_ == 0 or y_ == kuan - 1:
                    del dian[i]
                    del lenth[i]
            # print(dian)
            # print(lenth)
            # 绘线
            s = len(dian) - 1
            for i in range(0, s + 1, 1):
                (a, b) = dian[i]
                cv2.line(img, (a, b), (x, y), 1)
            # cv2.imshow('jieguo',img)
            # 极坐标转换
            for i in range(0, s + 1, 1):
                (a, b) = dian[i]
                if a > x and b < y:
                    jiao = math.asin((y - b) / lenth[i])
                elif a < x and b < y:
                    jiao = math.pi - math.asin((y - b) / lenth[i])
                elif a < x and b > y:
                    jiao = math.pi + math.asin((b - y) / lenth[i])
                else:
                    jiao = 1.5 * math.pi + math.asin((b - y) / lenth[i])
                dian[i] = (lenth[i], jiao)
            # print(dian)
            # 按极角冒泡排序
            for j in range(s, -1, -1):
                for i in range(0, j, 1):
                    (lenthi, jiaoi) = dian[i]
                    (lenthj, jiaoj) = dian[i + 1]
                    if jiaoi > jiaoj:
                        (a, b) = dian[i]
                        Lenthi = lenth[i]
                        dian[i] = dian[i + 1]
                        lenth[i] = lenth[i + 1]
                        dian[i + 1] = (a, b)
                        lenth[i + 1] = Lenthi
            # print(dian)
            for i in range(len(lenth) - 1, 0, -1):
                (chang1, jiao1) = dian[i]
                (chang2, jiao2) = dian[i - 1]
                if abs(jiao1 - jiao2) < 0.1:
                    del lenth[i]
                    del dian[i]
            # print(dian)
            for i in range(len(lenth) - 1, -1, -1):
                (chang1, jiao1) = dian[i]
                if jiao1 > math.pi:
                    del dian[i]
                    del lenth[i]
            # print(dian)
            # print(lenth)
            # 判断手势
            while len(dian) > 5:
                tmp = min(lenth)
                for i in range(len(dian) - 1, -1, -1):
                    if lenth[i] == tmp:
                        del lenth[i]
                        del dian[i]
            if len(dian) == 5:
                tmp = sorted(lenth)
                if lenth[0] > 0.6 * lenth[2] and lenth[1] > 0.8 * lenth[2] and (
                        lenth[2] > lenth[3] or lenth[2] > lenth[1]) and \
                        lenth[3] > 0.8 * lenth[2] and lenth[4] > 0.4 * lenth[2]:
                    HY[h] = 5
                elif lenth[0] > 0.6 * lenth[2] and lenth[1] > 0.8 * lenth[2] and (
                        lenth[2] > lenth[3] or lenth[2] > lenth[1]) and lenth[3] > 0.8 * lenth[2] and lenth[4] < 0.4 * \
                        lenth[2]:
                    HY[h] = 4
                elif lenth[0] < 0.6 * lenth[2] and lenth[1] > 0.8 * lenth[2] and (
                        lenth[2] > lenth[3] or lenth[2] > lenth[1]) and lenth[3] > 0.8 * lenth[2] and lenth[4] < 0.4 * \
                        lenth[2]:
                    HY[h] = 3
                elif tmp[-3] < 0.8 * tmp[-1] and tmp[-1] > 1.5 * maxdist and tmp[-2] > 0.8 * tmp[-1]:
                    for i in range(0, 5, 1):
                        if lenth[i] == tmp[-1]:
                            (rou1, jiao1) = dian[i]
                        elif lenth[i] == tmp[-2]:
                            (rou2, jiao2) = dian[i]
                    if abs(jiao1 - jiao2) > np.pi / 2:
                        HY[h] = 6
                    else:
                        HY[h] = 2
                elif tmp[-2] < 0.8 * tmp[-1] and tmp[-1] > 1.5 * maxdist:
                    HY[h] = 1
                elif tmp[-1] < 1.5 * maxdist:
                    HY[h] = 0
                else:
                    HY[h] = 6
            if len(dian) == 4:
                tmp = sorted(lenth)
                if lenth[0] > 0.6 * lenth[1] and lenth[2] > 0.8 * lenth[1] and (
                        lenth[1] > lenth[0] or lenth[1] > lenth[2]) and \
                        lenth[3] > 0.6 * lenth[1]:
                    HY[h] = 4
                elif lenth[0] < 0.6 * lenth[1] and lenth[2] > 0.8 * lenth[1] and (
                        lenth[1] > lenth[0] or lenth[1] > lenth[2]) and lenth[3] > 0.6 * lenth[1]:
                    HY[h] = 3
                elif tmp[-3] < 0.8 * tmp[-1] and tmp[-1] > 1.5 * maxdist and tmp[-2] > 0.8 * tmp[-1]:
                    for i in range(0, 4, 1):
                        if lenth[i] == tmp[-1]:
                            (rou1, jiao1) = dian[i]
                        elif lenth[i] == tmp[-2]:
                            (rou2, jiao2) = dian[i]
                    if abs(jiao1 - jiao2) > np.pi / 2:
                        HY[h] = 6
                    else:
                        HY[h] = 2
                elif tmp[-2] < 0.8 * tmp[-1] and tmp[-1] > 1.5 * maxdist:
                    HY[h] = 1
                elif tmp[-1] < 1.5 * maxdist:
                    HY[h] = 0
            if len(dian) == 3:
                tmp = sorted(lenth)
                if lenth[0] > 0.8 * lenth[1] and (lenth[1] > lenth[0] or lenth[1] > lenth[2]) and lenth[2] > 0.8 * \
                        lenth[1]:
                    HY[h] = 3
                elif tmp[-3] < 0.8 * tmp[-1] and tmp[-1] > 1.5 * maxdist and tmp[-2] > 0.8 * tmp[-1]:
                    for i in range(0, 3, 1):
                        if lenth[i] == tmp[-1]:
                            (rou1, jiao1) = dian[i]
                        elif lenth[i] == tmp[-2]:
                            (rou2, jiao2) = dian[i]
                    if abs(jiao1 - jiao2) > np.pi / 2:
                        HY[h] = 6
                    else:
                        HY[h] = 2
                elif tmp[-2] < 0.8 * tmp[-1] and tmp[-1] > 1.5 * maxdist:
                    HY[h] = 1
                elif tmp[-1] < 1.5 * maxdist:
                    HY[h] = 0
            if len(dian) == 2:
                tmp = sorted(lenth)
                if lenth[0] > 1.5 * maxdist and lenth[1] > 1.5 * maxdist:
                    (chang1, jiao1) = dian[0]
                    (chang2, jiao2) = dian[1]
                    if abs(jiao1 - jiao2) > np.pi / 2:
                        HY[h] = 6
                    else:
                        HY[h] = 2
                elif tmp[-1] > 1.5 * maxdist and tmp[-2] < 1.5 * maxdist:
                    HY[h] = 1
                elif tmp[-1] < 1.5 * maxdist:
                    HY[h] = 0
            if len(dian) == 1:
                if lenth[0] < 1.8 * maxdist:
                    HY[h] = 0
                else:
                    HY[h] = 1
            if len(dian) == 0:
                HY[h] = 0
            #####################################################################
            num = HY
        #print(num)
        #print(x_)
        #print(y_)
        ##########################################################################
        # 动作分割，以握拳（0号）为中断一个动作的截止标志，动态握拳为一个单词的结束标志
        for i in range(N - 1, 0, -1):
            if (num[i - 1] != num[i] and num[i + 1] != num[i] and num[i - 1] == num[i + 1]):
                del num[i]
                del x_[i]
                del y_[i]
                N = N - 1
        for i in range(N - 1, 0, -1):
            if (num[i - 1] != num[i] and num[i + 1] != num[i]):
                del num[i]
                del x_[i]
                del y_[i]
                N = N - 1
        #print(num)
        #print(x_)
        #print(y_)
        j = 1
        while (j < N):
            for i in range(j, N + 1, 1):  # 从第j个动作开始后检索握拳动作
                if num[i - 1] == 0:
                    Num = num[j - 1:i + 1]  # 两次中断动作之间的手势单独提取出来
                    Num1 = [Num.count(k) for k in set(Num)]
                    Num_max = max(Num1)
                    for ii in range(0, len(Num), 1):
                        k = Num[ii]
                        if (Num.count(k) == Num_max):
                            Nummax = k
                            break
                    ########################################
                    # 调用数据函数，查找相应手势Nummax代表的含义，并输出
                    X_ = x_[j - 1:i - 1]
                    Y_ = y_[j - 1:i - 1]
                    dongtai = 0
                    Hanyi_jing = ["", "a", "b", "c", "d", "e", "f"]
                    Hanyi_heng = ["v", "h", "i", "j", "k", "l", "m"]
                    Hanyi_shu = ["o", "n", "p", "q", "r", "s", "t"]
                    Hanyi_xie = [" ", "u", "g", "w", "x", "y", "z"]

                    if (max(X_) - min(X_)) > 30 and (max(Y_) - min(Y_)) > 30:
                        dongtai = 3
                    if (max(X_) - min(X_)) > 30 and (max(Y_) - min(Y_)) < 30:
                        dongtai = 1
                    if (max(X_) - min(X_)) < 30 and (max(Y_) - min(Y_)) > 30:
                        dongtai = 2

                    if dongtai == 0:
                        self.textEdit.insertPlainText("%s"%Hanyi_jing[Nummax])
                        #print(Hanyi_jing[Nummax], end="")
                    if dongtai == 1:
                        self.textEdit.insertPlainText("%s"%Hanyi_heng[Nummax])
                        #print(Hanyi_heng[Nummax], end="")
                    if dongtai == 2:
                        self.textEdit.insertPlainText("%s"%Hanyi_shu[Nummax])
                        #print(Hanyi_shu[Nummax], end="")
                    if dongtai == 3:
                        self.textEdit.insertPlainText("%s"%Hanyi_xie[Nummax])
                        #print(Hanyi_xie[Nummax], end="")
                    ########################################
                    # 判断握拳手势的结尾，以便下一个手势的检索
                    j = i
                    while (num[j - 1] == 0):
                        if j == N:
                            j = N + 1
                            break
                        else:
                            j = j + 1
                    X_ = x_[i - 1:j - 1]
                    Y_ = y_[i - 1:j - 1]
                    if (j - 1 == i):
                        continue
                    dongtai = 0
                    if (max(X_) - min(X_)) > 30 and (max(Y_) - min(Y_)) > 30:
                        dongtai = 3
                    if (max(X_) - min(X_)) > 30 and (max(Y_) - min(Y_)) < 30:
                        dongtai = 1
                    if (max(X_) - min(X_)) < 30 and (max(Y_) - min(Y_)) > 30:
                        dongtai = 2

                    if dongtai == 0:
                        self.textEdit.insertPlainText("%s"%Hanyi_jing[0])
                        #print(Hanyi_jing[0], end="")
                    if dongtai == 1:
                        self.textEdit.insertPlainText("%s"%Hanyi_heng[0])
                        #print(Hanyi_heng[0], end="")
                    if dongtai == 2:
                        self.textEdit.insertPlainText("%s"%Hanyi_shu[0])
                        #print(Hanyi_shu[0], end="")
                    if dongtai == 3:
                        self.textEdit.insertPlainText("%s"%Hanyi_xie[0])
                       # print(Hanyi_xie[0], end="")
                    break
        cv2.waitKey()
    
if __name__=="__main__": 
    import sys
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec())


