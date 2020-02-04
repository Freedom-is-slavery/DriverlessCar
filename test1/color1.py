import cv2 as cv
import  numpy as np


def video_color_revision():
    capture = cv.VideoCapture(0)
    #print(type(capture))
    while True:
        ret, frame = capture.read()
        if ret == False:
            break
        frame = cv.flip(frame, 1)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #分离红色
        lower_hsv1 = np.array([0,80,46])
        lower_hsv2 = np.array([156,80,46])
        upper_hsv1 = np.array([10,255,255])
        upper_hsv2 = np.array([180,255,255])

        #试验，提取皮肤
        lower_hsv = np.array([0,30,30])
        upper_hsv = np.array([40,170,255])

        #mask1 = cv.inRange(hsv, lowerb= lower_hsv1, upperb= upper_hsv1)
        #mask2 = cv.inRange(hsv, lowerb= lower_hsv2, upperb= upper_hsv2)
        skin_mask =  cv.inRange(hsv, lowerb= lower_hsv, upperb= upper_hsv)

        #mask = mask1 + mask2
        #dst = cv.bitwise_or(frame, frame, mask=mask)
        dst = cv.bitwise_and(frame, frame, mask= skin_mask)

        cv.imshow("raw video", frame)
        #cv.imshow("mask1 video", mask1)
        #cv.imshow("mask2 video", mask2)
        #cv.imshow("mask mixed", mask)
        #cv.imshow("red recognition", dst)
        cv.imshow("skin mask", skin_mask)
        cv.imshow("skin recognition", dst)

        c = cv.waitKey(40)

        if c == ord('q'):
            break

video_color_revision()

cv.waitKey(0)
cv.destroyAllWindows()