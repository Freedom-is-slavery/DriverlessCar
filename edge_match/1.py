import cv2 as cv
import numpy as np


for picnum_base in range(1, 5):
    read_path_mark = 'D:\\picbase\\mark_base\\' + str(picnum_base) + '.jpg'
    img = cv.imread(read_path_mark, 0)
    canny_base = cv.Canny(img, 50, 150)

cv.imshow('canny', canny_base)
_ , contours_base, hierarchy_base = cv.findContours(canny_base, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
print(len(contours_base))
capture = cv.VideoCapture(0)
while True:
    t1 = cv.getTickCount()  # 运行时间计算
    _ , frame = capture.read()
    t2 = cv.getTickCount()  # 运行时间计算
    c = cv.waitKey(40)
    t3 = cv.getTickCount()  # 运行时间计算
    if c == ord('q'):
        break

    #img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img, (5, 5), 0)
    canny = cv.Canny(img, 50, 150)

    _ , contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.imshow('Canny', canny)
    print(len(contours))
    ret = cv.matchShapes(contours[0], contours_base[0], 1, 0.0)
    print("match:", ret)
    t4 = cv.getTickCount()
    print("running time:", (t4 - t3 + t2 - t1) * 1000 / cv.getTickFrequency(), "ms")  # 给出运行时间
cv.waitKey(0)
cv.destroyAllWindows()
