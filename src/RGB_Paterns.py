import numpy as np
def Wrap_Around(Function_Points, LED_Patern_Points, Start):
    F=np.int64(np.size(Function_Points,1))
    P=np.int64(np.size(LED_Patern_Points,1))
    
    if F-(P-Start)>0:
        LED_Patern_Points[:,Start:P,:]=Function_Points[:,0:P-Start,:]
        LED_Patern_Points[:,0:F-(P-Start),:]=Function_Points[:,P-Start:,:]
    else:
        LED_Patern_Points[:,Start:Start+np.size(Function_Points,1),:]=Function_Points[:,:,:]
    return LED_Patern_Points