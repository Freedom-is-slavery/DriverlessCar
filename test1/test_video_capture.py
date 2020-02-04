import cv2
import  numpy as np

def video_demo():
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        cv2.imshow("video", frame)
        c = cv2.waitKey(500)

        if c == 8:
            break


def get_image_info(image):
    print("the type of image is:", type(image))
    print("the shape of image is:", image.shape)
    print("the size of image is:", image.size)
    print("the dtype of image is:", image.dtype)
    pixel_data = np.array(image)
    print("the pixel data is:", pixel_data)


im1 = cv2.imread("C:\\users\\admin\\desktop\\wallpaper\\1.jpg")
#get_image_info(im1)
#cv2.imshow("im1", im1)

video_demo()

cv2.waitKey(0)
cv2.destroyAllWindows()
