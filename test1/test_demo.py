import cv2 as cv
import numpy as np


picnum = 1
read_path = "C:\\Users\\admin\\Desktop\\wallpaper\\" + str(picnum) + ".jpg"
img = cv.imread(read_path)
cv.imshow("raw image", img)

cv.waitKey(0)
cv.destroyAllWindows()
