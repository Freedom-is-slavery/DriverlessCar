import cv2
import os
import numpy
import shutil

#将wallpaper文件夹下的所有图片经灰度化处理后放进其子文件夹
PictureNum = 1
ver = 1
ReadPath = "C:\\users\\admin\\desktop\\wallpaper\\" + str(PictureNum) + ".jpg"
WriteFold = "C:\\users\\admin\\desktop\\wallpaper\\greypicture"
WritePath = WriteFold + "\\" + str(ver) + ".jpg"

if not(os.path.exists(WriteFold)):
    os.makedirs(WriteFold)
    print("Now the folder {} has been created".format(WriteFold))
else:
    print("The folder {} already exists".format(WriteFold))


clr = input("Would you like to clear the folder?y/n\n")
if (clr == "y"):
    shutil.rmtree(WriteFold)
    os.makedirs(WriteFold)



while os.path.exists(ReadPath):
    img = cv2.imread(ReadPath)
    imggrey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    while os.path.exists(WritePath):
        ver = ver + 1
        WritePath = WriteFold + "\\" + str(ver) + ".jpg"

    cv2.imwrite(WritePath,imggrey,[int(cv2.IMWRITE_JPEG_QUALITY),100])
    PictureNum = PictureNum + 1
    ReadPath = "C:\\users\\admin\\desktop\\wallpaper\\" + str(PictureNum) + ".jpg"

