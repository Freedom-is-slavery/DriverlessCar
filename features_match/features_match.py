import cv2 as cv
from os import walk
import numpy as np
from os.path import join

#version:2.0
#计划改进：效率方面，事先计算库中的特征点数据，为树莓派的运算节省时间
#交通标志牌识别，模板库中共有6个交通标志，识别测试样例不包含极端特殊拍摄角度，成功率很高
#交警手势识别成功率很低


def video_demo():
    '''
    摄像头捕捉拍摄和照片存储

    '''
    picnum_cap = 1
    capture = cv.VideoCapture(0)
    while True:
        _ , frame = capture.read()
        cv.imshow("video", frame)

        c = cv.waitKey(500)
        if c == ord('q') or picnum_cap >= 20:
            break
        #摄像头拍摄的存储路径定义
        write_path = "D:\\picbase\\test\\capture\\" + str(picnum_cap) + ".jpg"
        cv.imwrite(write_path, frame)
        picnum_cap = picnum_cap + 1

#video_demo()

#摄像头捕捉到的图片存放的路径，并读入进行处理
picnum_captured = 13    #设定值，确定捕捉到的哪一张照片进行识别与处理
read_path_captured = "D:\\picbase\\test\\" + str(picnum_captured) + ".jpg"
img_captured = cv.imread(read_path_captured, 0)

height, width = img_captured.shape[:2]
print(width, height)

#尺度变换，在树莓派的摄像头640*480的分辨率下不需要（把下面这句话注释掉即可）
img_captured = cv.resize(img_captured, (int(0.3 * width), int(0.3 * height)), interpolation= cv.INTER_CUBIC)

#创建特征点描述对象，下列几种选一
orb = cv.ORB_create()       #采用ORB算法
sift = cv.xfeatures2d.SIFT_create()    #采用SIFT算法
t1 = cv.getTickCount()      #运行时间计算
#1.ORB算法检测特征点
kp_captured, des_captured = orb.detectAndCompute(img_captured, None)
#2.SIFT算法检测特征点
#kp_captured, des_captured = sift.detectAndCompute(img_captured, None)

t2 = cv.getTickCount()      #运行时间计算
#1.创建BF暴力匹配器，用于捕捉到的图和模板进行特征点匹配
bf = cv.BFMatcher(cv.NORM_HAMMING)

#2.定义FLANN匹配器
indexParams = dict(algorithm=0, trees=5)
searchParams = dict(checks=50)
flann = cv.FlannBasedMatcher(indexParams,searchParams)

folder_police_demo = 'D:\\picbase\\police_demo3'
folder_mark_demo = 'D:\\picbase\\mark_base'
descriptors_police_demo = []
descriptors_mark_demo = []

#获取交警手势特征数据文件
for (dirpath, dirnames, filenames) in walk(folder_police_demo):
    for f in filenames:
        if f.endswith("orb.npy"):
            descriptors_police_demo.append(f)
#获取交通标志特征数据文件
for (dirpath, dirnames, filenames) in walk(folder_mark_demo):
    for f in filenames:
        if f.endswith("orb.npy"):
            descriptors_mark_demo.append(f)

#最佳匹配初始化
most_match_number_mark = 0
best_picnum_mark = 0
most_match_number_police = 0
best_picnum_police = 0
match_description1 = ''
match_description2 = ''
fail_flag = 0
whistle_flag = 0
state = [0, 0, 0, 0]
#标志和手势动作描述，Tuple类型
mark_description = ['go straight', 'whistle', 'turn left', 'turn right', 'move right', 'move left']
police_description = ['go straight', 'move left', 'move right', 'slow down', 'stop', 'turn right', 'turn left']

print("base picture number | matched point number")
#在模板库中寻找特征点匹配程度最高的图片
#匹配交通标志
for picnum_base in range(1, 7):
    #使用 KNN 算法实现匹配
    #matches = flann.knnMatch(des1, des_captured, k = 2)
    matches = bf.knnMatch(np.load(join(folder_mark_demo, descriptors_mark_demo[picnum_base-1])), des_captured, k = 2)

    good_match = []
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good_match.append(m)

    if len(good_match) > most_match_number_mark:
        best_picnum_mark = picnum_base
        most_match_number_mark = len(good_match)

    print("{:8d}".format(picnum_base), "{}:{:8d}".format(mark_description[picnum_base-1], len(good_match)))

t3 = cv.getTickCount()      #运行时间计算
print("base picture number | matched point number")
#匹配交警手势
for picnum_base in range(1, 8):
    #使用 KNN 算法实现匹配
    #matches = flann.knnMatch(des1, des_captured, k = 2)
    matches = bf.knnMatch(np.load(join(folder_police_demo, descriptors_police_demo[picnum_base-1])), des_captured, k = 2)

    good_match = []
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good_match.append(m)

    if len(good_match) > most_match_number_police:
        best_picnum_police = picnum_base
        most_match_number_police = len(good_match)

    print("{:8d}".format(picnum_base), "{}:{:8d}".format(police_description[picnum_base-1], len(good_match)))

t4 = cv.getTickCount()      #运行时间计算
print("running time1:",(t2-t1)*1000/cv.getTickFrequency(), "ms")     #给出运行时间
print("running time2:",(t3-t2)*1000/cv.getTickFrequency(), "ms")     #给出运行时间
print("running time3:",(t4-t3)*1000/cv.getTickFrequency(), "ms")     #给出运行时间

img_captured_with_points = cv.drawKeypoints(img_captured, kp_captured, img_captured, color=(0, 255, 0), flags=0)

if most_match_number_police >= 7:       #阈值设定
    best_template_police = cv.imread("D:\\picbase\\police_demo3\\" + str(best_picnum_police) + ".jpg")
    print("matched demo in police: {}:{}".format(best_picnum_police, police_description[best_picnum_police-1]))
    print("most matched point number in police:", most_match_number_police)
    match_description1 = police_description[best_picnum_police-1]
else:
    fail_flag = fail_flag + 1
    print("No result for police!")

if most_match_number_mark >= 7:       #阈值设定
    best_template_mark = cv.imread("D:\\picbase\\mark_base\\" + str(best_picnum_mark) + ".jpg")
    print("matched demo in mark: {}:{}".format(best_picnum_mark, mark_description[best_picnum_mark-1]))
    print("most matched point number in mark:", most_match_number_mark)
    match_description2 = mark_description[best_picnum_mark-1]
else:
    fail_flag = fail_flag + 1
    print("No result for mark!")

demo_des1 = ['go straight', 'turn left', 'turn right', 'move left', 'move right']
demo_des2 = ['slow down', 'stop']
if fail_flag == 2:      #未识别到任何信号
    state = [0, 0, 0, 0]
else:                   #识别到信号
    if match_description2 == 'whistle':
        whistle_flag = 1
    if match_description1 != '':     #识别到需要交警手势优先的信号
        if match_description1 == demo_des1[0]:  #直行
            state = [0, 0, 0, 1]
        if match_description1 == demo_des1[1]:  #左转
            state = [0, 0, 1, 0]
        if match_description1 == demo_des1[2]:  #右转
            state = [0, 0, 1, 1]
        if match_description1 == demo_des1[3]:  #左变道未定义，默认为0000停止
            state = [0, 0, 0, 0]
        if match_description1 == demo_des1[4]:  #右变道未定义，默认为0000停止
            state = [0, 0, 0, 0]
        if match_description1 == demo_des2[0]:  #减速
            state = [0, 1, 0, 0]
        if match_description1 == demo_des2[1]:  #停止
            state = [0, 0, 0, 0]
    else:
        if match_description2 == demo_des1[0]:  #直行
            state = [0, 0, 0, 1]
        if match_description2 == demo_des1[1]:  #左转
            state = [0, 0, 1, 0]
        if match_description2 == demo_des1[2]:  #右转
            state = [0, 0, 1, 1]
        if match_description2 == demo_des1[3]:  #左变道未定义，默认为0000停止
            state = [0, 0, 0, 0]
        if match_description2 == demo_des1[4]:  #右变道未定义，默认为0000停止
            state = [0, 0, 0, 0]


t5 = cv.getTickCount()      #运行时间计算
print("running time4:",(t5-t4)*1000/cv.getTickFrequency(), "ms")     #给出运行时间

cv.namedWindow('points detected', cv.WINDOW_NORMAL)
cv.imshow('points detected', img_captured_with_points)
cv.waitKey(0)
cv.destroyAllWindows()

print("state:", state)
print("whistle flag:", whistle_flag)

