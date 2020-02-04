import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def skin_recognition_hsv(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_hsv = np.array([7, 28, 50])
    upper_hsv = np.array([20, 255, 255])

    skin_mask = cv.inRange(hsv, lowerb= lower_hsv, upperb= upper_hsv)
    cv.imshow("hsv mask", skin_mask)

#目前这种效果最好，即高斯滤波配合OTSU阈值分割算法对图像进行二值化处理
def skin_recognition_ycrcb_otsu(img):
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv.split(ycrcb)
    cr1 = cv.GaussianBlur(cr, (5,5), 0)
    _, skin_mask = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    cv.namedWindow("ycrcb otsu mask", cv.WINDOW_NORMAL)
    cv.imshow("ycrcb otsu mask", skin_mask)
    #skin = cv.bitwise_and(img, img, mask = skin_mask)
    #cv.imshow("ycrcb otsu skin", skin)
    return skin_mask

def skin_recognition_crcb(img):
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv.split(ycrcb)

    lower_ycrcb = np.array([0, 140, 100])
    upper_ycrcb = np.array([255, 175, 120])
    skin_mask = cv.inRange(ycrcb, lowerb= lower_ycrcb, upperb= upper_ycrcb)

    cv.imshow("crcb mask", skin_mask)

def template_match(mask, template, value):
    w, h = template.shape[::-1]
    res = cv.matchTemplate(mask, template, cv.TM_CCOEFF_NORMED)

    loc = np.where(res >= value)
    for pt in zip(*loc[::-1]):
        cv.rectangle(mask, pt, (pt[0] + w, pt[1]+ h), (255, 255, 255), 1)

    cv.namedWindow("detected mask", cv.WINDOW_NORMAL)
    cv.imshow("detected mask", mask)

#测试样例
picnum = 5
read_path = "D:\\picbase\\police\\" + str(picnum) + ".jpg"
write_path = "D:\\picbase\\police\\mask_demo" + str(picnum) + ".jpg"
#模板匹配的阈值
restriction = 0.7

#读入左转手势的黑白模板
left_demo_mask = cv.imread("D:\\picbase\\police\\left_demo.jpg",0)
img = cv.imread(read_path)

cv.namedWindow("raw image", cv.WINDOW_NORMAL)
cv.imshow("raw image", img)
cv.namedWindow("left demo", cv.WINDOW_NORMAL)
cv.imshow("left demo", left_demo_mask)

t1 = cv.getTickCount()

#skin_recognition_hsv(img)
img_mask = skin_recognition_ycrcb_otsu(img)
#skin_recognition_crcb(img)

template_match(img_mask, left_demo_mask, restriction)

t2 = cv.getTickCount()

print("running time:",(t2-t1)*1000/cv.getTickFrequency(), "ms")
cv.waitKey(0)
cv.destroyAllWindows()