import cv2 as cv
import numpy as np

#目前这种效果最好，即高斯滤波配合OTSU阈值分割算法对图像进行二值化处理
def skin_recognition_ycrcb_otsu(img):
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv.split(ycrcb)
    cr1 = cv.GaussianBlur(cr, (5,5), 0)
    _, skin_mask = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    #skin = cv.bitwise_and(img, img, mask = skin_mask)
    #cv.imshow("ycrcb otsu skin", skin)
    return skin_mask

#for picnum in range(1,8):
    #read_path = "D:\\picbase\\police\\demo" + str(picnum) + ".jpg"
    #write_path = "D:\\picbase\\police_mask\\" + str(picnum) + ".jpg"
    #img = cv.imread(read_path)
    #skin_mask = skin_recognition_ycrcb_otsu(img)
    #cv.imwrite(write_path, skin_mask)
t1 = cv.getTickCount()

for picnum in range(1,14):
    read_path = "D:\\picbase\\mark\\" + str(picnum) + ".jpg"
    write_path = "D:\\picbase\\mark_mask\\" + str(picnum) + ".jpg"
    img = cv.imread(read_path)
    skin_mask = skin_recognition_ycrcb_otsu(img)
    cv.imwrite(write_path, skin_mask)

t2 = cv.getTickCount()
print("running time:",(t2-t1)*1000/cv.getTickFrequency(), "ms")