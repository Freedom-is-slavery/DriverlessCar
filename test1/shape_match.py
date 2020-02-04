import cv2 as cv
import numpy as np

#先过一个高斯滤波会对图像的噪点起到很好的抑制作用
#配合自适应阈值OTSU算法使用
#返回一个二值化的黑白图像
def skin_recognition_ycrcb_otsu(img):
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv.split(ycrcb)
    cr1 = cv.GaussianBlur(cr, (5,5), 0)
    _, skin_mask = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    #cv.namedWindow("ycrcb otsu mask", cv.WINDOW_NORMAL)
    #cv.imshow("ycrcb otsu mask", skin_mask)

    return skin_mask


#write_path = "D:\\picbase\\police\\mask_demo" + str(picnum) + ".jpg"
#restriction = 0.65

#读入左转手势的黑白模板
left_demo_mask = cv.imread("D:\\picbase\\police_mask\\left_demo.jpg",0)


cv.namedWindow("left demo", cv.WINDOW_NORMAL)
cv.imshow("left demo", left_demo_mask)

t1 = cv.getTickCount()

match_degree = np.zeros([50])

base_setup = input("Would you like to set up a new picture base? y/n")
if base_setup == "y":
    for picnum in range(1,29):
        read_path = "D:\\picbase\\police\\" + str(picnum) + ".jpg"
        img = cv.imread(read_path)
        img_mask = skin_recognition_ycrcb_otsu(img)
        write_path = "D:\\picbase\\police_mask\\" + str(picnum) + ".jpg"
        cv.imwrite(write_path, img_mask)

for picnum in range(1, 29):
    match_degree[picnum] = cv.matchShapes(left_demo_mask, img_mask, 2, 0.0)
    print("match degree of picture %d:"%picnum, match_degree[picnum])

most_similar_degree = match_degree[1]
most_similar_picnum = 1
for i in range(1,29):
    if match_degree[i] < most_similar_degree:
        most_similar_degree = match_degree[i]
        most_similar_picnum = i

t2 = cv.getTickCount()

print("running time:",(t2-t1)*1000/cv.getTickFrequency(), "ms")
print("most similar degree:", most_similar_degree)
print("most similar picture number:", most_similar_picnum)

#namedWindow("most similar picture", cv.WINDOW_NORMAL)
#path = "D:\\picbase\\police\\" + str(most_similar_picnum) + ".jpg"
#cv.imshow("most similar picture", path)

cv.waitKey(0)
cv.destroyAllWindows()