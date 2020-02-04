import cv2 as cv
import numpy as np


most_match_number = 0
best_picnum = 1

picnum_captured = 20
read_path_captured = "D:\\picbase\\police\\" + str(picnum_captured) + ".jpg"


img_captured = cv.imread(read_path_captured)
height, width = img_captured.shape[:2]
print(width, height)
t1 = cv.getTickCount()
img_captured = cv.resize(img_captured, (int(0.3 * width), int(0.3 * height)), interpolation= cv.INTER_CUBIC)

#orb = cv.ORB_create()
sift = cv.xfeatures2d.SIFT_create()
kp_captured, des_captured = sift.detectAndCompute(img_captured, None)

index_params = dict(algorithm=0, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)

#kp2, des2 = orb.detectAndCompute(img_captured, None)
#bf = cv.BFMatcher(cv.NORM_HAMMING)
t2 = cv.getTickCount()

for picnum_base in range(1, 8):
    read_path_base = "D:\\picbase\\police_demo2\\demo" + str(picnum_base) + ".jpg"
    img_base = cv.imread(read_path_base)
    kp1, des1 = sift.detectAndCompute(img_base, None)
    #matches = bf.match(des1, des2)
    matches = flann.knnMatch(des1, des_captured, k = 2)

    img_points_base = cv.drawKeypoints(img_base, kp1, img_base, color=(0, 255, 0), flags=0)
    cv.imshow(str(picnum_base), img_points_base)

    good_match = [ ]
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good_match.append(m)

    if len(good_match) > most_match_number:
        best_picnum = picnum_base
        most_match_number = len(good_match)

    print(picnum_base, ":", len(good_match))

t3 = cv.getTickCount()
print("running time:",(t2-t1)*1000/cv.getTickFrequency(), "ms")
print("running time:",(t3-t2)*1000/cv.getTickFrequency(), "ms")

img_points_captured = cv.drawKeypoints(img_captured, kp_captured, img_captured, color=(0, 255, 0), flags=0)

print("matched demo number:", best_picnum)
print("most matched point number:", most_match_number)
cv.namedWindow('p1', cv.WINDOW_NORMAL)
cv.imshow('p1', img_points_captured)

cv.waitKey(0)
cv.destroyAllWindows()