# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:29:19 2022

@author: Joe
"""

import numpy as np
import colorsys


        
def HLS(H1,L1,H2,L2,S):
    Colorspace_Data=np.zeros((256, 256, 6)) #X,Y,[RGBHLS]
    HLS_Data=np.zeros((256, 256, 3)) #X,Y,[HLS]
    
    HLS_Data[:,0,0]=H1
    HLS_Data[0,:,1]=L1
    
    HLS_Data[:,255,0]=H2
    HLS_Data[255,:,1]=L2
    
    HLS_Data[:,:,2]=S #limited functionality, S is constant here
    
    Delta_H=(H2-H1)/255
    Delta_L=(L2-L1)/255
    
    
    #set H (X) first
    for X in range(1,256,1):
        if HLS_Data[0,X-1,0]+Delta_H<0:
            HLS_Data[:,X,0]=HLS_Data[:,X-1,0]+Delta_H + 1
        elif HLS_Data[0,X-1,0]+Delta_H>1:
            HLS_Data[:,X,0]=HLS_Data[:,X-1,0]+Delta_H - 1
        else:
            HLS_Data[:,X,0]=HLS_Data[:,X-1,0]+Delta_H
            
    #set L (Y)
    for Y in range(1,256,1):
        if HLS_Data[Y-1,0,1]+Delta_L<0:
            HLS_Data[Y,:,1]=HLS_Data[Y-1,:,1]+Delta_L + 1
        elif HLS_Data[Y-1,0,1]+Delta_L>1:
            HLS_Data[Y,:,1]=HLS_Data[Y-1,:,1]+Delta_L - 1
        else:
            HLS_Data[Y,:,1]=HLS_Data[Y-1,:,1]+Delta_L
            
    #convert HLS space to RGB space
    for X in range(0,256,1):
        for Y in range(0,256,1):
            Colorspace_Data[X,Y,0]=colorsys.hls_to_rgb(HLS_Data[X,Y,0],HLS_Data[X,Y,1],HLS_Data[X,Y,2])[0]
            Colorspace_Data[X,Y,1]=colorsys.hls_to_rgb(HLS_Data[X,Y,0],HLS_Data[X,Y,1],HLS_Data[X,Y,2])[1]
            Colorspace_Data[X,Y,2]=colorsys.hls_to_rgb(HLS_Data[X,Y,0],HLS_Data[X,Y,1],HLS_Data[X,Y,2])[2]
    
    Colorspace_Data[:,:,3:6]=HLS_Data[:,:,0:3]
    print('redrawing hls')
    return Colorspace_Data

HLS(0,0,1,1,1)