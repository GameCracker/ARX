#!/usr/bin/env python2

## Color Tracking v1.0
## Copyright (c) 2013-2014 Abid K and Jay Edry
## You may use, redistribute and/or modify this program it under the terms of the MIT license (https://github.com/abidrahmank/MyRoughWork/blob/master/license.txt).


''' v 0.1 - It tracks two objects of blue and yellow color each '''

import cv2
import numpy as np

def getthresholdedimg(hsv):
    yellow = cv2.inRange(hsv,np.array((0,120,100)),np.array((40,255,255)))
    blue = cv2.inRange(hsv,np.array((228,100,100)),np.array((255,255,255)))
    white = cv2.inRange(hsv,np.array((0,170,140)),np.array((255,255,255)))
    both = cv2.add(yellow, blue)
    both = cv2.add(both, white)
    return both

im = None

def click(event, x, y, flags, param):
    global im
    
    if event != cv2.EVENT_LBUTTONDOWN:
        return
        
    print('click!')
    print(im.item(x, y, 0), im.item(x, y, 1), im.item(x, y, 2))



c = cv2.VideoCapture(0)
width,height = c.get(3),c.get(4)
print "frame width and height : ", width, height

img = np.zeros((height,width,3), np.uint8)
# cv2.line(img,(0,0),(511,511),(255,255,255),5)

px, py = None, None

while(1):
    _,f = c.read()
    f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,5)
    im = hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    both = getthresholdedimg(hsv)
    erode = cv2.erode(both,None,iterations = 3)
    dilate = cv2.dilate(erode,None,iterations = 10)

    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    matched = False
    for cnt in contours:
        matched = True
        x,y,w,h = cv2.boundingRect(cnt)
        cx,cy = x+w/2, y+h/2

        cv2.rectangle(f,(x,y),(x+w,y+h),[0,255,255],2)

        if px is not None:
            cv2.line(img, (px, py), (cx, cy), (255, 255, 255), 2)
        
        px, py = cx, cy
        
    if not matched:
        px = py = None

    f = cv2.add(f, img)

    cv2.imshow('img2', erode)
    
    cv2.imshow('img',f)
    cv2.setMouseCallback('img', click)

    if cv2.waitKey(25) == 27:
        break

    if cv2.waitKey(25) == 99:
        img = np.zeros((height,width,3), np.uint8)        
        


    
cv2.destroyAllWindows()
c.release()
