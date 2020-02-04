import cv2
import time
  
clicked = False  
def onMouse(event, x, y, flags, param):  
    global clicked  
    if event == cv2.EVENT_LBUTTONUP:  
        clicked = True  
  
cameraCapture = cv2.VideoCapture(cv2.CAP_DSHOW)
cameraCapture.set(3, 176)
cameraCapture.set(4, 144) # 帧宽度和帧高度都设置为100像素
cv2.namedWindow('MyWindow',cv2.WINDOW_NORMAL)
cv2.setMouseCallback('MyWindow', onMouse)
print('showing camera feed. Click window or press and key to stop.')  
success, frame = cameraCapture.read()  
print(success)
time.sleep(5)
count = 0  
while success and cv2.waitKey(500) == -1 and not clicked:
    cv2.imshow('MyWindow', frame)
    success, frame = cameraCapture.read()  
    name = 'D:\\picbase\\test\\capture\\image' + str(count) + '.jpg'
    cv2.imwrite(name,frame)
    count += 1

print(frame.shape)
cv2.destroyWindow('MyWindow')  
cameraCapture.release()  
