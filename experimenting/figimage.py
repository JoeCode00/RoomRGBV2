# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 23:53:10 2022

@author: Joe
"""

import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import time

Colorspace_Values_Init=np.zeros((256,256,3))
Colorspace_Values_Init[:,:,0]=1

Fig=[0]*1
Fig[0]=plt.figure()
Fig[0].canvas.draw()
Colorspace_Img=plt.figimage(Colorspace_Values_Init,xo=200,yo=200,alpha=1,origin='lower')

plt.show()
Fig[0].canvas.flush_events()

time.sleep(2)

Colorspace_Values_Init[:,:,0]=0
Colorspace_Values_Init[:,:,1]=1

Colorspace_Img.set_data(Colorspace_Values_Init)

Fig[0].canvas.flush_events()