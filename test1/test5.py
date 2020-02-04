import cv2 as cv
import numpy as np

img = np.zeros([400,400,3], np.uint8)
img[: , : , 1] = np.ones([400,400]) * 255
cv.imshow("new image", img)

#print(type(img))
#print(img.shape[0])

#pixel_data = np.array(img)
print("pixel data:\n", np.array(img))

time0 = cv.getTickCount()
img = cv.bitwise_not(img)
time1 = cv.getTickCount()

time = (time1 - time0)/ cv.getTickFrequency()

cv.imshow("reverse image", img)

#下面两种print的方式结果是一样的
print("pixel data reversed:\n", np.array(img))
print("img:\n", img)

print("time of bit reverse: %s ms"%(time))
cv.waitKey(0)
cv.destroyAllWindows()