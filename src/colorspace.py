import numpy as np
import colorsys

def Black():
    Colorspace_Data=np.zeros((256, 256, 6)) #X,Y,[RGBHLS]
    print('redrawing black')
    return Colorspace_Data

def HLS(X1,Y1,X2,Y2):
    Colorspace_Data=np.zeros((256,256,6))
    
    mgrid=np.mgrid[Y1:Y2:256j,X1:X2:256j] #dontworryboutit
    #mgrid=np.mgrid[]
    Colorspace_Data[:,:,3]=mgrid[1,:,:]
    Colorspace_Data[:,:,4]=mgrid[0,:,:]
    Colorspace_Data[:,:,5]=1

    for X in range(0,256,1):
        for Y in range(0,256,1):
            RGB=colorsys.hls_to_rgb(Colorspace_Data[X,Y,3],Colorspace_Data[X,Y,4],Colorspace_Data[X,Y,5])
            Colorspace_Data[X,Y,0]=RGB[0]
            Colorspace_Data[X,Y,1]=RGB[1]
            Colorspace_Data[X,Y,2]=RGB[2]
    print('redrawing hls')
    return Colorspace_Data
