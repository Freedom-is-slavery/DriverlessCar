import cv2 as cv

for picnum in range(1, 8):
    read_path= "D:\\picbase\\police_demo2\\demo" + str(picnum) + ".jpg"
    img  = cv.imread(read_path)
    height, width = img.shape[:2]
    img = cv.resize(img, (int(0.8 * width), int(0.8 * height)), interpolation=cv.INTER_CUBIC)
    cv.imwrite(read_path, img)