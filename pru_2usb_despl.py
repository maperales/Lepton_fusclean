#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:50:55 2019

@author: mpe
"""
import cv2
import numpy as np
cv2.namedWindow("TERMICA", cv2.WINDOW_NORMAL)
cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("MIX", cv2.WINDOW_NORMAL)

cameraID1=0
cameraID2=0
for idx in range(1,8):
    testv=cv2.VideoCapture(idx)
    if testv.isOpened():
        rval, frametest=testv.read()
        an,alt,kk=frametest.shape
        if an is 120:
            print("Lepton Cam Found in port %d" %idx)
            cameraID2=idx
        else:
            print("WebCam (%dx%d) found in port %d" %(an, alt, idx))
            cameraID1=idx
        
vcv = cv2.VideoCapture(cameraID1)
vct = cv2.VideoCapture(cameraID2)
if vcv.isOpened(): # try to get the first frame
    rval, frame = vcv.read()
else:
    rval = False
    
if vct.isOpened(): # try to get the first frame
    rval2, framet = vct.read()
else:
    rval2 = False

DX=0
DY=0
while rval and rval2:
    res = cv2.resize(framet,None,fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
    filas,cols,kk=frame.shape
    M=cv2.getRotationMatrix2D(((cols-1)/2.0,(filas-1)/2.0),90,1)
    framer=cv2.warpAffine(frame,M,(cols, filas))
    Mt=np.float32([[1,0,DX],[0,1,DY]])
    res=cv2.warpAffine(res,Mt,(cols,filas))
    #framer=cv2.rotate(frame,90)
   # vis = cv2.resize(frame, (640,480),interpolation=cv2.INTER_CUBIC)
    cv2.imshow("TERMICA", res)
    cv2.imshow("preview", framer)
    dst = cv2.addWeighted(framer,0.5,res,0.5,0)
    cv2.imshow('MIX',dst)     
    rval, frame = vcv.read()
    rval2, framet = vct.read()

    key = cv2.waitKey(20)
    if key == 119:
        DY = DY-10
    if key == 115:
        DY = DY+10
    if key == 97:
        DX = DX -10
    if key == 100:
        DX = DX+10
    if key == 27: # exit on ESC
        break
cv2.destroyAllWindows()
vcv.release
vct.release
print("DX:%d DY: %d" %(DX, DY))

