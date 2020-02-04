import cv2 as cv
import  numpy as np

#对两幅图进行像素级别的加减乘除的算术运算操作
def add_demo(im1, im2):
    dst = cv.add(im1, im2)
    cv.imshow("add", dst)

def subtract_demo(im1, im2):
    dst = cv.subtract(im1, im2)
    cv.imshow("subtract", dst)

def multiply_demo(im1, im2):
    dst = cv.multiply(im1, im2)
    cv.imshow("multiply", dst)

def divide_demo(im1, im2):
    dst = cv.divide(im1, im2)
    cv.imshow("divide", dst)

def pic_mean(img):
    '''
    计算均值与方差
    '''
    mean, dev = cv.meanStdDev(img)
    for i in range(3):
        print("mean of channel {}:".format(i), mean[i])
        print("dev of channel {}".format(i), dev[i])

def contrast_brightness_demo(img, c, b, name):
    '''
    调整亮度和对比度，亮度调整即add操作，对比度调整即像素成倍放大操作，拉大像素差异
    '''
    blank = np.zeros(img.shape, img.dtype)
    dst = cv.addWeighted(img, c, blank, 1-c, b)
    cv.imshow("brightness dst of %s"%name, dst)
read_path1 = "C:\\Users\\admin\\Desktop\\wallpaper\\1.jpg"
read_path2 = "C:\\Users\\admin\\Desktop\\wallpaper\\2.jpg"
img1 = cv.imread(read_path1)  #读1.jpg
img2 = cv.imread(read_path2)  #读2.jpg
print(img1.shape[:3])
print(img2.shape[:3])

#add_demo(img1, img2)
#subtract_demo(img1, img2)
#multiply_demo(img1, img2)
#divide_demo(img1,img2)
pic_mean(img1)
pic_mean(img2)

cv.imshow("raw picture", img1)
contrast_brightness_demo(img1, 1, 0, "dst1")
contrast_brightness_demo(img1, 1.5, 0, "dst2")

#cv.imshow("black image", empty_image)

cv.waitKey(0)
cv.destroyAllWindows()
