#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:10:16 2019

@author: mpe
"""

# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""


# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps 
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

def gstreamer_pipeline (capture_width=320, capture_height=240, display_width=320, display_height=240, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! '    
    'video/x-raw(memory:NVMM), '     
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print( gstreamer_pipeline(flip_method=0))
    cv2.namedWindow("TERMICA")
    cv2.namedWindow("MIX", cv2.WINDOW_NORMAL)
    cameraID = 1
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    vc = cv2.VideoCapture(cameraID)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
        if cap.isOpened():
            window_handle = cv2.namedWindow('REAL', cv2.WINDOW_AUTOSIZE)
            # Window 
            while cv2.getWindowProperty('REAL',0) >= 0:
                ret_val, img = cap.read();
                cv2.imshow('REAL',img)
                res = cv2.resize(frame,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
                cv2.imshow("TERMICA", res)
                rval, frame = vc.read()
                dst = cv2.addWeighted(img,0.5,res,0.5,0)
                cv2.imshow('MIX',dst)
                # exit on ESC
                # This also acts as 
                keyCode = cv2.waitKey(30) & 0xff
                # Stop the program on the ESC key
                if keyCode == 27:
                   break
           
        else:
            print ('CSI_CAM NO FUNCIONA')
    else:
        print("USB CAM no funciona")
    cap.release()
    vc.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    show_camera()