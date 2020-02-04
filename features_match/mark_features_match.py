import cv2 as cv
from matplotlib import pyplot as plt

#version 1.5
#计划改进：效率方面，事先计算库中的特征点数据，为树莓派的运算节省时间
#交通标志牌识别，模板库中共有6个交通标志
#识别测试样例不包含极端特殊拍摄角度，成功率很高
#！！很严重的问题，直行、靠左行驶、靠右行驶不能有效辨别，推测是因为形状一模一样
#偷懒的解决办法：把靠左和靠右行驶扔掉，换别的交通标识

def video_demo():
    '''
    摄像头捕捉拍摄和照片存储

    '''
    picnum_cap = 1
    capture = cv.VideoCapture(0)
    while True:
        _ , frame = capture.read()
        cv.namedWindow('video',cv.WINDOW_NORMAL)
        frame = cv.flip(frame, 1)
        cv.imshow("video", frame)

        c = cv.waitKey(40)
        if c == ord('q'):
            write_path = "D:\\picbase\\test\\capture\\" + str(picnum_cap) + ".jpg"
            cv.imwrite(write_path, frame)
            break


mark_description = ['go straight', 'whistle', 'turn left', 'turn right', 'move right', 'move left']

video_demo()

#摄像头捕捉到的图片存放的路径，并读入进行处理
picnum_captured = 1
read_path_captured = "D:\\picbase\\test\\capture\\" + str(picnum_captured) + ".jpg"
img_captured = cv.imread(read_path_captured)


height, width = img_captured.shape[:2]
print(width, height)

#尺度变换，在树莓派的摄像头640*480的分辨率下不需要（把下面这句话注释掉即可）
#img_captured = cv.resize(img_captured, (int(0.3 * width), int(0.3 * height)), interpolation= cv.INTER_CUBIC)
#创建ORB特征点描述对象
orb = cv.ORB_create()
sift = cv.xfeatures2d.SIFT_create()




t2 = cv.getTickCount()      #运行时间计算
#ORB算法检测特征点
kp_captured, des_captured = sift.detectAndCompute(img_captured, None)
#1.创建BF暴力匹配器，用于捕捉到的图和模板进行特征点匹配
bf = cv.BFMatcher(cv.NORM_L2)

indexParams = dict(algorithm=0, trees=5)
searchParams = dict(checks=50)
#2.定义FLANN匹配器
flann = cv.FlannBasedMatcher(indexParams,searchParams)

most_match_number = 0
best_picnum = None

print("base picture number | matched point number")
#在模板库中寻找特征点匹配程度最高的图片
for picnum_base in range(1, 7):
    read_path_base = "D:\\picbase\\mark_base\\" + str(picnum_base) + ".jpg"
    img1 = cv.imread(read_path_base)
    kp1, des1 = sift.detectAndCompute(img1, None)
    #使用k-最近邻匹配方式
    # 使用 KNN 算法实现匹配
    matches = flann.knnMatch(des1, des_captured, k = 2)
    #matches = bf.knnMatch(des1, des_captured, k = 2)
    img_points_base = cv.drawKeypoints(img1, kp1, img1, color=(0, 255, 0), flags=0)
    cv.imshow(str(picnum_base), img_points_base)

    good_match = [ ]
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good_match.append(m)

    if len(good_match) > most_match_number:
        best_picnum = picnum_base
        most_match_number = len(good_match)

    print("{:8d}".format(picnum_base), "{}:{:8d}".format(mark_description[picnum_base-1], len(good_match)))
t3 = cv.getTickCount()      #运行时间计算
print("running time:",(t3-t2)*1000/cv.getTickFrequency(), "ms")     #给出运行时间

img = cv.drawKeypoints(img_captured, kp_captured, img_captured, color=(0, 255, 0), flags=0)
best_template = cv.imread("D:\\picbase\\mark_base\\" + str(best_picnum) + ".jpg")
print("matched demo: {}:{}".format(best_picnum, mark_description[best_picnum-1]))
print("most matched point number:", most_match_number)

cv.namedWindow('points detected', cv.WINDOW_NORMAL)
cv.imshow('points detected', img)
cv.waitKey(0)
cv.destroyAllWindows()