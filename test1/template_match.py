import cv2 as cv
import numpy as np

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

#def template_match(mask, template):
    #w, h = template.shape[::-1]
    #res = cv.matchTemplate(mask, template, cv.TM_CCOEFF_NORMED)


#测试样例
picnum = 15000
read_path = "D:\\picbase\\test\\capture_police\\police_go_straight\\img" + str(picnum) + ".jpg"
write_path = "D:\\picbase\\police\\mask_demo" + str(picnum) + ".jpg"

#读入左转手势的黑白模板
left_demo_mask = cv.imread("D:\\picbase\\police_mask\\left_demo.jpg",0)
img = cv.imread(read_path)

cv.namedWindow("raw image", cv.WINDOW_NORMAL)
cv.imshow("raw image", img)


t1 = cv.getTickCount()

img_mask = skin_recognition_ycrcb_otsu(img)
cv.imshow('img_mask', img_mask)

#template_match(img_mask, left_demo_mask)

t2 = cv.getTickCount()

print("running time:",(t2-t1)*1000/cv.getTickFrequency(), "ms")
cv.waitKey(0)
cv.destroyAllWindows()