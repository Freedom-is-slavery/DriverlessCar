import cv2 as cv
import  numpy as np
import os
import shutil


def video_capture_write():
    capture = cv.VideoCapture(0)
    pic_num = 1
    while(capture.isOpened()):
        key_flag = cv.waitKey(40)

        ret, frame = capture.read()
        frame = cv.flip(frame, 1)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # 试验，分离肤色
        lower_hsv = np.array([0, 28, 50])
        upper_hsv = np.array([20, 255, 255])

        skin_mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
        img_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("raw video", frame)
        cv.imshow("grey video", img_grey)
        cv.imshow("mask video", skin_mask)

        if key_flag == ord('c'):
            cv.imwrite(write_path + "\\raw\\raw" + str(pic_num) + ".jpg", frame)
            mean, dev = cv.meanStdDev(frame)
            print("BGR通道均值：", mean)
            print("BGR通道方差：", dev)
            cv.imwrite(write_path + "\\skin_mask\\" + str(pic_num) + ".jpg", skin_mask)
            pic_num = pic_num + 1

        #键入q表示退出,跳出循环
        if key_flag == ord('q'):
            break


write_path = "D:\\picbase\\test"
if not(os.path.exists(write_path)):
    os.makedirs(write_path)

clr1 = input("Would you like to clear the raw folder?y/n\n")
if (clr1 == "y"):
    shutil.rmtree(write_path + "\\raw")
    os.makedirs(write_path + "\\raw")
clr2 = input("Would you like to clear the skin_mask folder?y/n\n")
if (clr2 == "y"):
    shutil.rmtree(write_path + "\\skin_mask")
    os.makedirs(write_path + "\\skin_mask")

video_capture_write()

cv.waitKey(0)
cv.destroyAllWindows()