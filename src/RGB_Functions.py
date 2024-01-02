import numpy as np
import colorsys

def Dist_Line(Colorspace_Data, Function_Points, Points, X1, Y1, X2, Y2):
    X_Array=np.uint8(np.round(np.linspace(X1,X2,Points)*255))
    Y_Array=np.uint8(np.round(np.linspace(Y1,Y2,Points)*255))

    for P in np.arange(Points):
        P=np.uint64(np.round(P))
        Function_Points[0,P,:]=Colorspace_Data[Y_Array[P],X_Array[P],0:3]
        
    return Function_Points

class Two_Tones():
    def __init__(self, Buffer_Color, X1, Y1, X2, Y2, Func_Frame, Speed, Function_Points, parent=None):
        super(Two_Tones, self).__init__()
        self.Function_Points_HLS=np.zeros(np.shape(Function_Points))
        self.Function_Points=np.zeros(np.shape(Function_Points))
        self.Loop_Length = int((101-Speed)*100)
        self.Loop_Frame = int(Func_Frame % self.Loop_Length)
        
        if Buffer_Color=="Black":
            self.Buffer_Lum=0
        elif Buffer_Color=="White":
            self.Buffer_Lum=1
        
        self.Color_1=            np.array([0.0,0.2])*self.Loop_Length #.2
        self.Color_1_To_Buffer=   np.array([0.2,0.3])*self.Loop_Length 
        self.Buffer_1=           np.array([0.3,0.4])*self.Loop_Length 
        self.Buffer_To_Color_2=     np.array([0.4,0.5])*self.Loop_Length 
        self.Color_2=              np.array([0.5,0.7])*self.Loop_Length #.2
        self.Color_2_To_Buffer=     np.array([0.7,0.8])*self.Loop_Length 
        self.Buffer_2=           np.array([0.8,0.9])*self.Loop_Length 
        self.Buffer_To_Color_1=   np.array([0.9,1.0])*self.Loop_Length 
        
        
        
        if self.Loop_Frame>=self.Color_1[0] and self.Loop_Frame<=self.Color_1[1]:
            self.Function_Points_HLS[:,:,0]=X1
            self.Function_Points_HLS[:,:,1]=Y1
            self.Function_Points_HLS[:,:,2]=1
        
        elif self.Loop_Frame>self.Color_1_To_Buffer[0] and self.Loop_Frame<=self.Color_1_To_Buffer[1]:
            self.Function_Points_HLS[:,:,0]=X1
            self.Function_Points_HLS[:,:,2]=1
            
            self.L1=Y1
            self.L2=self.Buffer_Lum
            self.A=self.Color_1_To_Buffer[0]
            self.B=self.Color_1_To_Buffer[1]
            
            self.Function_Points_HLS[:,:,1]=self.Line()
            
        elif self.Loop_Frame>self.Buffer_1[0] and self.Loop_Frame<=self.Buffer_1[1]:
            self.Function_Points_HLS[:,:,0]=X1
            self.Function_Points_HLS[:,:,1]=self.Buffer_Lum
            self.Function_Points_HLS[:,:,2]=1
        
        elif self.Loop_Frame>self.Buffer_To_Color_2[0] and self.Loop_Frame<=self.Buffer_To_Color_2[1]:
            self.Function_Points_HLS[:,:,0]=X2
            self.Function_Points_HLS[:,:,2]=1
            
            self.L1=self.Buffer_Lum
            self.L2=Y2
            self.A=self.Buffer_To_Color_2[0]
            self.B=self.Buffer_To_Color_2[1]
            
            self.Function_Points_HLS[:,:,1]=self.Line()
        
        elif self.Loop_Frame>self.Color_2[0] and self.Loop_Frame<=self.Color_2[1]:
            self.Function_Points_HLS[:,:,0]=X2
            self.Function_Points_HLS[:,:,1]=Y2
            self.Function_Points_HLS[:,:,2]=1
        
        elif self.Loop_Frame>self.Color_2_To_Buffer[0] and self.Loop_Frame<=self.Color_2_To_Buffer[1]:
            self.Function_Points_HLS[:,:,0]=X2
            self.Function_Points_HLS[:,:,2]=1
            
            self.L1=Y2
            self.L2=self.Buffer_Lum
            self.A=self.Color_2_To_Buffer[0]
            self.B=self.Color_2_To_Buffer[1]
            
            self.Function_Points_HLS[:,:,1]=self.Line()
            
        elif self.Loop_Frame>self.Buffer_2[0] and self.Loop_Frame<=self.Buffer_2[1]:
            self.Function_Points_HLS[:,:,0]=Y2
            self.Function_Points_HLS[:,:,1]=self.Buffer_Lum
            self.Function_Points_HLS[:,:,2]=1
    
        elif self.Loop_Frame>self.Buffer_To_Color_1[0] and self.Loop_Frame<=self.Buffer_To_Color_1[1]:
            self.Function_Points_HLS[:,:,0]=X1
            self.Function_Points_HLS[:,:,2]=1
            
            self.L1=self.Buffer_Lum
            self.L2=Y1
            self.A=self.Buffer_To_Color_1[0]
            self.B=self.Buffer_To_Color_1[1]
            
            self.Function_Points_HLS[:,:,1]=self.Line()
            
        for i in range(np.shape(self.Function_Points_HLS)[1]):
            self.Function_Points[0,i,0]=colorsys.hls_to_rgb(self.Function_Points_HLS[0,i,0], self.Function_Points_HLS[0,i,1], self.Function_Points_HLS[0,i,2])[0]
            self.Function_Points[0,i,1]=colorsys.hls_to_rgb(self.Function_Points_HLS[0,i,0], self.Function_Points_HLS[0,i,1], self.Function_Points_HLS[0,i,2])[1]
            self.Function_Points[0,i,2]=colorsys.hls_to_rgb(self.Function_Points_HLS[0,i,0], self.Function_Points_HLS[0,i,1], self.Function_Points_HLS[0,i,2])[2]
    
    def Line(self):
        self.M=((self.L2-self.L1)/(self.B-self.A))
        return self.M*(self.Loop_Frame-self.A)+self.L1 #https://www.desmos.com/calculator/28kwl0fqe8