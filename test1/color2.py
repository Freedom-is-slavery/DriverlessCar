import cv2 as cv
import numpy as np

def color_split():
    capture = cv.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if ret == False:
            break
        frame = cv.flip(frame, 1)

        b, g, r = cv.split(frame)

        cv.imshow("blue", b)
        cv.imshow("green", g)
        cv.imshow("red", r)

        c = cv.waitKey(40)
        if c  == ord('q'):
            break

color_split()
cv.waitKey(0)
cv.destroyAllWindows()