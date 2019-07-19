#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:50:55 2019

@author: mpe
"""
import cv2

cv2.namedWindow("preview")
cameraID = 1
vc = cv2.VideoCapture(cameraID)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    res = cv2.resize(frame,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    cv2.imshow("preview", res)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break