import cv2 as cv
import numpy as np
from os import walk
from os.path import join

#提前计算特征点数据，提高程序运行效率

def create_descriptors(folder):
    '''
    创建描述子
    :param folder:
    :return: None
    '''
    files = []
    for (dirpath, dirnames, filenames) in walk(folder):
        files.extend(filenames)
    print(files)
    for f in files:
        if '.jpg' in f:
            save_descriptor(folder, f, cv.xfeatures2d.SIFT_create())

def save_descriptor(folder, image_path, feature_detector):
    '''
    保存特征描述文件
    :param folder:
    :param image_path:
    :param feature_detector:
    :return: None
    '''
    # 判断图片是否为orb.npy格式
    if image_path.endswith("sift"):
        return
    # 读取图片并检查特征
    img = cv.imread(join(folder,image_path))
    keypoints, descriptors = feature_detector.detectAndCompute(img, None)
    # 设置文件名并将特征数据保存到npy文件
    descriptor_file = image_path.replace("jpg", "sift")
    np.save(join(folder, descriptor_file), descriptors)

if __name__=='__main__':
    path = 'D:\\picbase\\police_demo3'
    create_descriptors(path)