'''
可視覺化的小工具
利用滑桿來控制想要得數值

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

# BGR to HSV
def toHSV(img):
     img_copy = img.copy()
     img_HSV = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
     return img_HSV

# get specify color mask
def getHsvMask(img):
     h_min = cv2.getTrackbarPos('HUE Min', 'TrackerBar')
     h_max = cv2.getTrackbarPos('HUE Max', 'TrackerBar')
     s_min = cv2.getTrackbarPos('SAT Min', 'TrackerBar')
     s_max = cv2.getTrackbarPos('SAT Max', 'TrackerBar')
     v_min = cv2.getTrackbarPos('VALUE Min', 'TrackerBar')
     v_max = cv2.getTrackbarPos('VALUE Max', 'TrackerBar')
     lowerWhite = np.array([h_min, s_min, v_min])
     upperWhite = np.array([h_max, s_max, v_max])
     maskWhite = cv2.inRange(img, lowerWhite, upperWhite)

     return maskWhite

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
          img_HSV = toHSV(frame)
          HSV_mask = getHsvMask(img_HSV)
          frame = drawpoint(frame, ValTrackers(frame))
          cv2.imshow('frame', frame)
          cv2.imshow('ROI', img_roi)
          cv2.imshow('HSV mask', HSV_mask)

          if cv2.waitKey(10) == ord('q'):
               break

if __name__ == '__main__':
     main()