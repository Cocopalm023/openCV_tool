'''
可視覺化的ROI小工具
利用滑桿來控制想保留的區域

2023/01/20 3:50
create by LYZ
'''
import cv2
import numpy as np


# Don't care
def passFunction(x):
     pass

# initialize TrackerBar
def initializeTrackerBar(img):
     windowName = 'TrackerBar'
     cv2.namedWindow(windowName)
     cv2.resizeWindow(windowName, 640, 200)
     cv2.createTrackbar('Width Top', windowName, 200, img.shape[1]//2, passFunction)
     cv2.createTrackbar('Height Top', windowName, 10, img.shape[0], passFunction)
     cv2.createTrackbar('Width Bottom', windowName, 200, img.shape[1]//2, passFunction)
     cv2.createTrackbar('Height Bottom', windowName, 100, img.shape[0], passFunction)

# Get Region of interesting
def getROI(img):
     height = img.shape[0]
     width = img.shape[1]
     triangle = np.array([ValTrackers(img)], dtype=np.int32)
     black_img = np.zeros_like(img)
     mask = cv2.fillPoly(black_img, triangle, 255)
     masked_img = cv2.bitwise_and(img, mask)
     return masked_img

# Get the trackerBar value
def ValTrackers(img):
     windowName = 'TrackerBar'
     widthTop = cv2.getTrackbarPos('Width Top', windowName)
     heightTop = cv2.getTrackbarPos('Height Top', windowName)
     widthBottom = cv2.getTrackbarPos('Width Bottom', windowName)
     heightBottom = cv2.getTrackbarPos('Height Bottom', windowName)

     points = np.float32([(widthBottom, heightBottom), (widthTop, heightTop), (img.shape[1] - widthTop, heightTop), (img.shape[1] - widthBottom, heightBottom)])
     return points

# Draw the points on the frame 
def drawpoint(img, points):
     picture = img
     for i in range(4):
          cv2.circle(picture, (int(points[i][0]), int(points[i][1])), 15, (0, 0, 255), cv2.FILLED)
     
     return picture

def main():
     cap = cv2.VideoCapture(0)
     if not cap.isOpened():
          print("Cannot open camera")
          exit()
     ret, frame = cap.read()
     initializeTrackerBar(frame)
     while(True):
          ret, frame = cap.read()
          if not ret:
               print("Can't receive frame (stream end?). Exiting ...")
               break
          gray = frame.copy()
          gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
          img_roi = getROI(gray)
          frame = drawpoint(frame, ValTrackers(frame))
          cv2.imshow('frame', frame)
          cv2.imshow('ROI', img_roi)

          if cv2.waitKey(10) == ord('q'):
               break

if __name__ == '__main__':
     main()