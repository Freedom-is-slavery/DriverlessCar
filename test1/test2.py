import os
import cv2
import numpy as np

im1 = cv2.imread("C:\\Users\\admin\\Desktop\\wallpaper\\3.jpg")
im2 = cv2.resize(im1,(1024,512),interpolation=cv2.INTER_CUBIC)
print("the shape of image 1 is:{}".format(im1.shape))
print("the shape of image 2 is:{}".format(im2.shape))

emptyImage1 = np.zeros(im1.shape, np.uint8) 
emptyImage2 = im1.copy()
emptyImage3 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
#emptyImage3[...] = 0

cv2.imshow("image copied",emptyImage2)
cv2.imshow("image black",emptyImage3)

picver = 0
picpath = "C:\\Users\\admin\\Desktop\\wallpaper\\3revised" + str(picver) + ".jpg"

#cv2.imshow("img1", emptyImage3)

#cv2.imshow("img2", im2)

cv2.waitKey(0)
cv2.destroyAllWindows()
