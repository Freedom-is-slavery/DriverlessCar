import cv2
import numpy as np
#from matplotlib import pyplot as plt

################################################################################

print('Load Image')

imgFile = 'spl23.jpg'

# load an original image
imge = cv2.imread(imgFile)
row = imge.shape[0]
col = imge.shape[1]
img = cv2.resize(imge, (int(col / 10), int(row / 10)))
################################################################################

print('YCbCr-RGB Skin Model')

rows, cols, channels = img.shape
################################################################################

# convert color space from rgb to ycbcr
imgYcc = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

# convert color space from bgr to rgb
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# prepare an empty image space
imgSkin = np.zeros(img.shape, np.uint8)
# copy original image
imgSkin = img.copy()
################################################################################

for r in range(rows):
    for c in range(cols):

        # non-skin area if skin equals 0, skin area otherwise
        skin = 0
        ########################################################################

        # get values from rgb color space
        R = img.item(r, c, 0)
        G = img.item(r, c, 1)
        B = img.item(r, c, 2)

        # get values from ycbcr color space
        Y = imgYcc.item(r, c, 0)
        Cr = imgYcc.item(r, c, 1)
        Cb = imgYcc.item(r, c, 2)
        ########################################################################

        # skin color detection

        if R > G and R > B:
            if (G >= B and 5 * R - 12 * G + 7 * B >= 0) or (G < B and 5 * R + 7 * G - 12 * B >= 0):
                if Cr > 135 and Cr < 180 and Cb > 85 and Cb < 135 and Y > 80:
                    skin = 1
                    # print 'Skin detected!'

        if 0 == skin:
            imgSkin.itemset((r, c, 0), 0)
            imgSkin.itemset((r, c, 1), 0)
            imgSkin.itemset((r, c, 2), 0)

# display original image and skin image
################################################################################
#cv2.imshow('imSkin', imgSkin)
#cv2.imwrite('rst4.jpg', imgSkin)
#cv2.waitKey(0)
imgSkin = cv2.cvtColor(imgSkin, cv2.COLOR_BGR2GRAY)
ret1, th1 = cv2.threshold(imgSkin, 85, 255, cv2.THRESH_BINARY)
kernel = np.ones((5, 5), np.uint8)
closing = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
(_, cnts, _) = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]  # 找到第一大的轮廓
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))
Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = 10 * min(Xs)
x2 = 10 * max(Xs)
y1 = 10 * min(Ys)
y2 = 10 * max(Ys)
hight = y2 - y1
width = x2 - x1
cropImg = img[y1+1:y1 + hight-1, x1+1:x1 + width-1]
cv2.imshow("closing",closing)
cv2.imshow("rs",cropImg)
print('Goodbye!')
cv2.waitKey(0)