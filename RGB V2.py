from src.rasppi import Initialize_Rasppi, send
from src.stream_analyzer import Stream_Analyzer

import src.colorspace as cs
import src.RGB_Functions as RGB_Func
import src.RGB_Paterns as RGB_Pat
import src.LED_Physical_Strip as LED_Physical_Strip

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget
    
from pyqtgraph.Qt import QtCore, QtWidgets

from functools import partial
import os

import time
import sys
import numpy as np
import argparse
import colorsys

global N_LEDS_Display

global K107A
K107A=False

if K107A:
    N_LEDS_Display=444

global Circle
Circle=True

if Circle:
    N_LEDS_Display=600
    
global Frame
Frame=0        
    
def Get_Frame():
    global Frame
    Frame=Frame+1
    return Frame-1

def init_FFT():
    args = parse_fft_args()
    window_ratio = convert_window_ratio(args.window_ratio)

    ear = Stream_Analyzer(
        #device = args.device,        # Pyaudio (Portaudio) device index, defaults to first mic input
        
        
        device = 1,
                    
                    
                    
                    
        rate   = 48000,               # Audio samplerate, None uses the default source settings
        FFT_window_size_ms  = 60,    # Window size used for the FFT transform
        updates_per_second  = 10000,  # How often to read the audio stream for new data
        # smoothing_length_ms = 50,    # Apply some temporal smoothing to reduce noisy features
        smoothing_length_ms = 5,    # Apply some temporal smoothing to reduce noisy features
        n_frequency_bins = args.frequency_bins, # The FFT features are grouped in bins
        visualize = 0,               # Visualize the FFT features with PyGame
        verbose   = args.verbose,    # Print running statistics (latency, FPS, ...)
        height    = args.height,     # Height, in pixels, of the visualizer window,
        window_ratio = window_ratio  # Float ratio of the visualizer window. e.g. 24/9
        )
    return ear, args

def parse_fft_args():
    FFT_Bins=1000
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=None, dest='device',
                        help='pyaudio (Portaudio) device index')
    parser.add_argument('--height', type=int, default=450, dest='height',
                        help='height, in pixels, of the visualizer window')
    parser.add_argument('--n_frequency_bins', type=int, default=FFT_Bins, dest='frequency_bins',
                        help='The FFT features are grouped in bins')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--window_ratio', default='24/9', dest='window_ratio',
                        help='float ratio of the visualizer window. e.g. 24/9')
    parser.add_argument('--sleep_between_Frames', dest='sleep_between_Frames', action='store_true',
                        help='when true process sleeps between Frames to reduce CPU usage (recommended for low update rates)')
    return parser.parse_args() 

def convert_window_ratio(window_ratio):
    if '/' in window_ratio:
        dividend, divisor = window_ratio.split('/')
        try:
            float_ratio = float(dividend) / float(divisor)
        except:
            raise ValueError('window_ratio should be in the format: float/float')
        return float_ratio
    raise ValueError('window_ratio should be in the format: float/float')
    
class Top_Widget(QWidget):
    def __init__(self, parent=None):
        super(Top_Widget, self).__init__(parent=parent)
        self.horizontalLayout = QHBoxLayout(self)
        self.Music = Music_Col()
        self.horizontalLayout.addWidget(self.Music)
        
        self.Main = Main_Col()
        self.horizontalLayout.addWidget(self.Main)
        
        self.Colorspace = Colorspace_Col()
        self.horizontalLayout.addWidget(self.Colorspace)
        
        self.Effect = Effect_Col()
        self.horizontalLayout.addWidget(self.Effect)
        
        self.Function = Function_Col()
        self.horizontalLayout.addWidget(self.Function)
        
        self.Patern = Patern_Col()
        self.horizontalLayout.addWidget(self.Patern)
        
        self.Mirror = Mirror_Col()
        self.horizontalLayout.addWidget(self.Mirror)
        
class Music_Col(QWidget):
    def __init__(self, parent=None):
        super(Music_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        
        # self.win = pyqtgraph.GraphicsLayoutWidget(title="Basic plotting examples")
        # self.horizontalLayout.addWidget(self.win)
        # self.p6 = self.win.addPlot(title="My Plot")
        # self.curve = self.p6.plot(pen='r')
        
        
        self.Music_Slider_Title = ['Peaking  ', #0
                                    'Agro  ',
                                    'Freq Low  ',
                                    'Freq High  ',
                                    'Bump  ',
                                    'Banger Point'
                                    ]
        
                    #min value, max value, initial value%
        self.Music_Slider_Info = [[1, 300, 25], #Peaking cant be 0
                                  [1.0, 24,  10], #Agro
                                  [0,  800, 20],#Freq Low 
                                  [1,  800, 100],#Freq High
                                  [0, 1, 0],
                                  [0, 0.999,50],
                                  ]
        self.Music_N_slider = len(self.Music_Slider_Title)
        self.Slider_Array=[0]*self.Music_N_slider
        for i in np.arange(self.Music_N_slider):
            self.min = self.Music_Slider_Info[i][0]
            self.max = self.Music_Slider_Info[i][1]
            self.current = self.Music_Slider_Info[i][2]
            self.slider_title = self.Music_Slider_Title[i]
            self.Slider_Array[i] = Slider(self.min, self.max, self.slider_title, None)
            
            self.Slider_Array[i].slider.setValue(int(self.current))
  
            self.verticalLayout.addWidget(self.Slider_Array[i])
            self.verticalLayout.addWidget(self.Slider_Array[i].slider)
            
            
        #Quit Button
        self.Quit_Stream=QtWidgets.QPushButton('Quit Stream')
        self.verticalLayout.addWidget(self.Quit_Stream)
        self.Quit_Stream.clicked[bool].connect(partial(self.Press_Button, 'Quit Stream')) 
        self.Quit_Stream.setStyleSheet("background-color : #F75757")
        spacerItem1 = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.verticalLayout.addItem(spacerItem1)
        
        self.Quit_Server=QtWidgets.QPushButton('Quit Server')
        self.Quit_Server.clicked[bool].connect(partial(self.Press_Button, 'Quit Server')) 
        self.Quit_Server.setStyleSheet("background-color : #CC0A0A")
        self.verticalLayout.addWidget(self.Quit_Server)
        self.verticalLayout.addItem(spacerItem1)
            
    def Press_Button(self, Pressed_Button_Title):
        global Quit_State
        Quit_State = Pressed_Button_Title
        print('A Quit Button Was Pushed:')
        print(Quit_State)
        
class Main_Col(QWidget):
    def __init__(self, parent=None):
        super(Main_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        self.Main_Slider_Title = ['Master Brightness', #0
                                 'X1  ',
                                 'Y1  ',
                                 'X2  ',
                                 'Y2  ',
                                 'Points  ', #5
                                 'Start  ',
                                 'Speed  '
                                 ]
        
                    #min value, max value, %Full scale initially
        self.Main_Slider_Info = [[0,1,0.5],#0
                               [0, 1, 0],
                               [0, 1, 0],
                               [0, 1, 1],
                               [0, 1, 1],
                               [1, N_LEDS_Display, 100], #5
                               [0, N_LEDS_Display, 0],
                               [0, 100, 50],
                               ]
        
        self.Main_N_slider = len(self.Main_Slider_Title)
        self.Slider_Array=[0]*self.Main_N_slider
        for i in np.arange(self.Main_N_slider):
            self.min = self.Main_Slider_Info[i][0]
            self.max = self.Main_Slider_Info[i][1]
            self.current = self.Main_Slider_Info[i][2]
            self.slider_title = self.Main_Slider_Title[i]
            self.Slider_Array[i]= Slider(self.min, self.max, self.slider_title, None)
    
            self.Slider_Array[i].slider.setValue(int(self.current*100))   
            self.verticalLayout.addWidget(self.Slider_Array[i])
            self.verticalLayout.addWidget(self.Slider_Array[i].slider)

class Slider(QWidget):
    def __init__(self, minimum, maximum, title, parent=None):
        super(Slider, self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.Title = QLabel(title)
        self.horizontalLayout.addWidget(self.Title)
        spacerItem = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.label = QLabel(self)
        self.horizontalLayout.addWidget(self.label)
        
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        
        self.resize(self.sizeHint())
        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())
        #spacerItem1 = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)  
        
        #self.verticalLayout.addItem(spacerItem1)
    
    def setLabelValue(self, value):
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
        self.maximum - self.minimum)
        self.label.setText(" {0:.4g}".format(self.x))
        
# self.win = pyqtgraph.GraphicsLayoutWidget(title="Basic plotting examples")
# self.horizontalLayout.addWidget(self.win)
# self.p6 = self.win.addPlot(title="My Plot")
# self.curve = self.p6.plot(pen='r')

class Colorspace_Col(QWidget):
    def __init__(self, parent=None):
        super(Colorspace_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        
        self.Colorspace_Button_Title = ['Black',
                                    'HLS',
                                    'O & B',
                                    'Hot',
                                    'Warm',
                                    'Cool',
                                    'Pink',  
                                    ]
        
        self.N_Buttons=len(self.Colorspace_Button_Title)
        self.Button_Array=[0]*self.N_Buttons
        for i in np.arange(self.N_Buttons):
            self.Button_Array[i] = QtWidgets.QPushButton(self.Colorspace_Button_Title[i])
            self.verticalLayout.addWidget(self.Button_Array[i])
            self.Button_Array[i].clicked[bool].connect(partial(self.Press_Button, self.Colorspace_Button_Title[i]))
    
    def Press_Button(self, Pressed_Button_Title):
        global Colorspace_Current
        Colorspace_Current=Pressed_Button_Title
        
        for j in np.arange(self.N_Buttons):
            if self.Colorspace_Button_Title[j]==Colorspace_Current:
                self.Button_Array[j].setStyleSheet("background-color : gray")
            else:
                self.Button_Array[j].setStyleSheet("background-color : #FF8989")
        
        global Colorspace_Data
        if Colorspace_Current=='Black':   
            Colorspace_Data=cs.Black()
        elif Colorspace_Current=='HLS':
            Colorspace_Data=cs.HLS(0,0,1,1)
        elif Colorspace_Current=='Hot':
            Colorspace_Data=cs.HLS(0,0,0.15,1)
        elif Colorspace_Current=='Warm':
            Colorspace_Data=cs.HLS(0.15,0,0.4,1)
        elif Colorspace_Current=='Cool':
            Colorspace_Data=cs.HLS(0.4,0,0.7,1)
        elif Colorspace_Current=='Pink':
            Colorspace_Data=cs.HLS(0.7,0,0.95,1)
        
        
        print('Set Colorspace: ', Colorspace_Current)
        print(' ')
        
class Effect_Col(QWidget):
    def __init__(self, parent=None):
        super(Effect_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        
        self.Effect_Button_Title = ['No Effect',
                                    'X2-.5',
                                    'X2-.25',
                                    'X2=X1',
                                    'X2+.25',
                                    'X2+.5',
                                    'Y2=Y1',
                                    'Y=0.5',
                                    ]
        
        self.N_Buttons=len(self.Effect_Button_Title)
        self.Button_Array=[0]*self.N_Buttons
        for i in np.arange(self.N_Buttons):
            self.Button_Array[i] = QtWidgets.QPushButton(self.Effect_Button_Title[i])
            self.verticalLayout.addWidget(self.Button_Array[i])
            self.Button_Array[i].clicked[bool].connect(partial(self.Press_Button, self.Effect_Button_Title[i]))
            
    def Press_Button(self, Pressed_Button_Title):
        global Effect_Current
        Effect_Current=Pressed_Button_Title
        for j in np.arange(self.N_Buttons):
            if self.Effect_Button_Title[j]==Effect_Current:
                self.Button_Array[j].setStyleSheet("background-color : gray")
            else:
                self.Button_Array[j].setStyleSheet("background-color : #FFFF89")
       
        print('Set Effect: ', Effect_Current)
        print(' ') 
       

class Function_Col(QWidget):
    def __init__(self, parent=None):
        super(Function_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        
        self.Function_Button_Title = ['Dist Line',
                                    'Music',
                                    'Two Tones W',
                                    'Two Tones B',
                                    '',
                                    ]
        
        self.N_Buttons=len(self.Function_Button_Title)
        self.Button_Array=[0]*self.N_Buttons
        for i in np.arange(self.N_Buttons):
            self.Button_Array[i] = QtWidgets.QPushButton(self.Function_Button_Title[i])
            self.verticalLayout.addWidget(self.Button_Array[i])
            self.Button_Array[i].clicked[bool].connect(partial(self.Press_Button, self.Function_Button_Title[i]))
    
    def Press_Button(self, Pressed_Button_Title):
        global Function_Current
        Function_Current=Pressed_Button_Title
        
        for j in np.arange(self.N_Buttons):
            if self.Function_Button_Title[j]==Function_Current:
                self.Button_Array[j].setStyleSheet("background-color : gray")
            else:
                self.Button_Array[j].setStyleSheet("background-color : #8CFF89")
        
        print('Set Function: ', Function_Current)
        print(' ')  
            
class Patern_Col(QWidget):
    def __init__(self, parent=None):
        super(Patern_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        
        self.Patern_Button_Title = ['Static',
                                    'Wrap Around',
                                    'Banger Point',
                                    'Banger Average',
                                    'Repeat',
                                    'Repeat Mirror',
                                    ]
        
        self.N_Buttons=len(self.Patern_Button_Title)
        self.Button_Array=[0]*self.N_Buttons
        for i in np.arange(self.N_Buttons):
            self.Button_Array[i] = QtWidgets.QPushButton(self.Patern_Button_Title[i])
            self.verticalLayout.addWidget(self.Button_Array[i])
            self.Button_Array[i].clicked[bool].connect(partial(self.Press_Button, self.Patern_Button_Title[i]))
            
    def Press_Button(self, Pressed_Button_Title):
        global Patern_Current
        Patern_Current=Pressed_Button_Title
        
        for j in np.arange(self.N_Buttons):
            if self.Patern_Button_Title[j]==Patern_Current:
                self.Button_Array[j].setStyleSheet("background-color : gray")
            else:
                self.Button_Array[j].setStyleSheet("background-color : #89FFFC")
        
        print('Set Patern: ', Patern_Current)
        print(' ')
            

             
            
class Mirror_Col(QWidget):
    def __init__(self, parent=None):
        super(Mirror_Col, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout(self)
        
        self.Mirror_Button_Title = ['No Mirror',
                                    'Full Mirror',
                                    'L to R',
                                    'R to L',
                                    '',
                                    '',
                                    ]
        
        self.N_Buttons=len(self.Mirror_Button_Title)
        self.Button_Array=[0]*self.N_Buttons
        for i in np.arange(self.N_Buttons):
            self.Button_Array[i] = QtWidgets.QPushButton(self.Mirror_Button_Title[i])
            self.verticalLayout.addWidget(self.Button_Array[i])
            self.Button_Array[i].clicked[bool].connect(partial(self.Press_Button, self.Mirror_Button_Title[i]))

    def Press_Button(self, Pressed_Button_Title):
        global Mirror_Current
        Mirror_Current=Pressed_Button_Title
        
        for j in np.arange(self.N_Buttons):
            if self.Mirror_Button_Title[j]==Mirror_Current:
                self.Button_Array[j].setStyleSheet("background-color : gray")
            else:
                self.Button_Array[j].setStyleSheet("background-color : #898FFF")
        
        print('Set Mirror: ', Mirror_Current)
        print(' ') 

    
def Music(Colorspace_Data, Function_Points, Points, Bump, X1, Y1, X2, Y2, Peaking, Agro, Cuttoff, Freq_Low, Freq_High, ear):
    Raw_FFTx, Raw_FFT, Binned_FFTx, Binned_FFT = ear.get_audio_features()
    
    Pre_Color_Space=np.zeros(Points)
    Freq_Range=Freq_High-Freq_Low
    Cut_Off_FFT=Binned_FFT[Freq_Low:Freq_High]
    Interpolated_FFT=np.interp(np.linspace(0,Freq_Range,Points),np.arange(Freq_Range),Cut_Off_FFT)
    
    Bump_FFT=np.sum(Interpolated_FFT)/100000000

    if Bump_FFT>1:
        print('Bump FFT > 1')
    Scaled_FFT=np.zeros(np.size(Interpolated_FFT))
    
    for i in range(np.size(Interpolated_FFT)):
        Scaled_FFT[i]=max(min(Interpolated_FFT[i]/(Peaking*200),1),0)
    
    Function_Points_HLS=np.zeros(np.shape(Function_Points))
    for i in range(Points):
        Pre_Color_Space[i]=Agro_Func(Scaled_FFT[i],Agro,Cuttoff)
        XN, YN = Single_Point_On_Line(Pre_Color_Space[i],X1,Y1,X2,Y2)
        X=np.uint8(np.round(YN*255))
        Y=np.uint8(np.round(XN*255))
        Function_Points_HLS[0,i,:]=Colorspace_Data[X,Y,3:6]
        Function_Points_HLS[0,i,1]=max(min(Function_Points_HLS[0,i,1]+Bump_FFT*Bump,1),0)
        
        Function_Points[0,i,0]=colorsys.hls_to_rgb(Function_Points_HLS[0,i,0], Function_Points_HLS[0,i,1], Function_Points_HLS[0,i,2])[0]
        Function_Points[0,i,1]=colorsys.hls_to_rgb(Function_Points_HLS[0,i,0], Function_Points_HLS[0,i,1], Function_Points_HLS[0,i,2])[1]
        Function_Points[0,i,2]=colorsys.hls_to_rgb(Function_Points_HLS[0,i,0], Function_Points_HLS[0,i,1], Function_Points_HLS[0,i,2])[2]
        
    
    return Function_Points

def Agro_Func(Volume_In, Agro, Cuttoff):
    return  max(min(((2**(Agro*Volume_In))-1)*(2**(1-1.2*Agro))-Cuttoff,1),0)

def Single_Point_On_Line(data_point,X1,Y1,X2,Y2):
    line_length=((abs(X2-X1)**2)+(abs(Y2-Y1)**2))**(1/2)
    if X2==X1:
        XN=X1
        if Y2>Y1:
            YN=Y1+data_point*line_length
        else:
            YN=Y1-data_point*line_length
    else:
        M=(Y2-Y1)/(X2-X1)
        XN=X1+(X2-X1)*data_point
        YN=M*(XN-X1)+Y1
    return XN, YN

# def XY_Manipulate(N_LEDS_Display,Frame, Speed, X1, Y1, X2, Y2, Mode):
#     if Mode == 'LR':
#         a = 5*(N_LEDS_Display-Speed)
        
#         func_X1 = ((Frame-(a*X1)) % (2*a))/a #https://www.desmos.com/calculator/fd5tntpfks
#         if func_X1 <= 1:
#             X1 = func_X1
#         else:
#             X1 = 2-func_X1
        
#         func_X2 = ((Frame-(a*X2)) % (2*a))/a
#         if func_X2 <= 1:
#             X2 = func_X2
#         else:
#             X2 = 2-func_X2
        
#     return X1, Y1, X2, Y2


global LED_Patern_Points_Old
LED_Patern_Points_Old = np.zeros((1,N_LEDS_Display,3)) 
    

#init fig here
app = QtWidgets.QApplication(sys.argv)
global w
w = Top_Widget()
w.show()


# super(Initialize_Func, self).__init__(parent=parent)
Colorspace_Data=np.zeros((256, 256, 6))

ear, args = init_FFT()

IP='169.254.48.122'
Port=20150
#/home/pi/Desktop/V4_Server.py

global clientSocket #for quitting

clientSocket = Initialize_Rasppi(IP,Port)

S=np.zeros(1)

global Quit_State
Quit_State = 'On'

w.Colorspace.Press_Button('HLS')
w.Function.Press_Button('Music')
w.Patern.Press_Button('Static')
w.Effect.Press_Button('No Effect')
w.Mirror.Press_Button('No Mirror')


class Main_Func():
    def __init__(self, parent=None):
        super(Main_Func, self).__init__()
        self.Func_Frame = Get_Frame()        

        #poll all sliders
        self.Master_Brightness_Slider= w.Main.Slider_Array[0]
        self.X1_Slider = w.Main.Slider_Array[1]
        self.Y1_Slider = w.Main.Slider_Array[2]
        self.X2_Slider = w.Main.Slider_Array[3]
        self.Y2_Slider = w.Main.Slider_Array[4]
        self.Points_Slider = w.Main.Slider_Array[5]
        self.Start_Slider = w.Main.Slider_Array[6]
        self.Speed_Slider = w.Main.Slider_Array[7]
        
        self.Master_Brightness= self.Master_Brightness_Slider.x
        self.X1 = self.X1_Slider.x
        self.Y1 = self.Y1_Slider.x
        self.X2 = self.X2_Slider.x
        self.Y2 = self.Y2_Slider.x
        self.Points = np.uint64(np.round(self.Points_Slider.x))
        self.Start = np.int64(np.round(self.Start_Slider.x))
        self.Speed = np.int64(np.round(self.Speed_Slider.x))
        
        self.Peaking_Slider =       w.Music.Slider_Array[0]
        self.Agro_Slider =          w.Music.Slider_Array[1]
        self.Freq_Low_Slider =      w.Music.Slider_Array[2]
        self.Freq_High_Slider =     w.Music.Slider_Array[3]
        self.Bump_Slider =          w.Music.Slider_Array[4]
        self.Banger_Point_Slider =  w.Music.Slider_Array[5]
        
        self.Peaking =   self.Peaking_Slider.x
        self.Agro =      self.Agro_Slider.x
        self.Freq_Low =  np.uint64(np.round(self.Freq_Low_Slider.x))
        self.Freq_High = np.uint64(np.round(self.Freq_High_Slider.x))
        self.Bump =      self.Bump_Slider.x
        self.Banger_Point = self.Banger_Point_Slider.x
        
        # print('Colorspace: ', Colorspace_Current)
        # print('Function: ', Function_Current)     
        # print('Patern: ', Patern_Current) 
        # print('Effect: ', Effect_Current)
        # print(' ')
        
        # if Effect_Current=='XY Bump LR':
        #     self.X1, self.Y1, self.X2, self.Y2, = XY_Manipulate(N_LEDS_Display, self.Func_Frame, self.Speed, self.X1, self.Y1, self.X2, self.Y2, 'LR')    
        
        if Colorspace_Current=='O & B':
            w.Colorspace.Press_Button('HLS')
            
            self.X1=13/360 #Orange
            self.Y1=.4
            self.X2=228/360 #Blue
            self.Y2=.324
            
            self.X1_Slider.slider.setValue(int(self.X1*100))
            self.Y1_Slider.slider.setValue(int(self.Y1*100))
            self.X2_Slider.slider.setValue(int(self.X2*100))
            self.Y2_Slider.slider.setValue(int(self.Y2*100))
        
        if Effect_Current == 'X2=X1':
            self.X2=self.X1
            self.X2_Slider.slider.setValue(int(self.X2*100))   
        elif Effect_Current == 'X2+.25':
            self.X2=self.X1+.25
            if self.X2>1:
                self.X2=1
            self.X2_Slider.slider.setValue(int(self.X2*100))  
        elif Effect_Current == 'X2+.5':
            self.X2=self.X1+.5
            if self.X2>1:
                self.X2=1
            self.X2_Slider.slider.setValue(int(self.X2*100))  
        elif Effect_Current == 'X2-.25':
            self.X2=self.X1-.25
            if self.X2<0:
                self.X2=0
            self.X2_Slider.slider.setValue(int(self.X2*100))
        elif Effect_Current == 'X2-.5':
            self.X2=self.X1-.5
            if self.X2<0:
                self.X2=0
            self.X2_Slider.slider.setValue(int(self.X2*100))    
        elif Effect_Current == 'Y2=Y1':
            self.Y2=self.Y1
            self.Y2_Slider.slider.setValue(int(self.Y2*100))
            
        elif Effect_Current == 'Y=0.5':
            self.Y1=0.5
            self.Y2=0.5
            self.Y1_Slider.slider.setValue(int(self.Y1*100))
            self.Y2_Slider.slider.setValue(int(self.Y2*100))
            w.Effect.Press_Button('No Effect')
        
        #function
        self.Function_Points = np.zeros((1,self.Points,3))    
        if Function_Current=='Dist Line':
            self.Function_Points = RGB_Func.Dist_Line(Colorspace_Data, self.Function_Points, self.Points, self.X1, self.Y1, self.X2, self.Y2)
        elif Function_Current=='Easy Horiz':
            self.X1=0
            self.Y1=0.5
            self.X2=1
            self.Y2=0.5
            
            self.X1_Slider.slider.setValue(int(self.X1*100))
            self.Y1_Slider.slider.setValue(int(self.Y1*100))
            self.X2_Slider.slider.setValue(int(self.X2*100))
            self.Y2_Slider.slider.setValue(int(self.Y2*100))
            
            self.Function_Points = RGB_Func.Dist_Line(Colorspace_Data, self.Function_Points, self.Points, self.X1, self.Y1, self.X2, self.Y2)
        elif Function_Current=='Music':
            self.Function_Points = Music(Colorspace_Data, self.Function_Points, self.Points, self.Bump, self.X1, self.Y1, self.X2, self.Y2, self.Peaking, self.Agro, 0.005, self.Freq_Low, self.Freq_High, ear)
            
        elif Function_Current=='Two Tones W':
            self.Function_Points=RGB_Func.Two_Tones('White',self.X1, self.Y1, self.X2, self.Y2, self.Func_Frame, self.Speed, self.Function_Points).Function_Points
        elif Function_Current=='Two Tones B':
            self.Function_Points=RGB_Func.Two_Tones('Black',self.X1, self.Y1, self.X2, self.Y2, self.Func_Frame, self.Speed, self.Function_Points).Function_Points
        
        self.Function_Points_Average=np.zeros((1,1,3))
        for i in range(1):
            self.Function_Points_Average[0,0,i]=np.average(self.Function_Points[:,:,i])
        #patern
        self.LED_Patern_Points = np.zeros((1,N_LEDS_Display,3))  
        if Patern_Current=='Static':
            self.LED_Patern_Points = RGB_Pat.Wrap_Around(self.Function_Points, self.LED_Patern_Points, self.Start)
            self.Points_Slider.slider.setValue(int(100))
            
        elif Patern_Current=='Wrap Around':
            if Patern_Current=='Wrap Around':
                self.Start_Offset=int((self.Func_Frame*((self.Speed**1.5)/100))%N_LEDS_Display)
                self.S=self.Start_Offset+self.Start
                while self.S>N_LEDS_Display:
                    self.S=self.S-N_LEDS_Display
                self.Start=np.uint32(self.S)
                self.LED_Patern_Points = RGB_Pat.Wrap_Around(self.Function_Points, self.LED_Patern_Points, self.Start)
                
        elif Patern_Current=='Banger Point' or Patern_Current=='Banger Average':
            self.Banger_Speed=int(self.Speed/5)
            global LED_Patern_Points_Old
            
            if Patern_Current=='Banger Point':
                self.Banger_Point_LEDs=self.Function_Points[0,int(self.Points*self.Banger_Point),:]*self.Banger_Speed
            elif Patern_Current=='Banger Average':
                self.Banger_Point_LEDs=self.Function_Points_Average[0,0,:]*self.Banger_Speed
                
            self.LED_Patern_Points=np.roll(LED_Patern_Points_Old,self.Banger_Speed,axis=1)
            self.LED_Patern_Points[0,:self.Banger_Speed,:]=self.Banger_Point_LEDs
            
            time.sleep(0.01)
            
        elif Patern_Current=='Repeat' or Patern_Current=='Repeat Mirror':
            self.Repeat_Length=np.shape(self.Function_Points)[1] #probably equal to Points
            self.N_Full_Repeats=int(np.floor(N_LEDS_Display/(self.Repeat_Length)))
            self.Extra_Points_Needed=int(N_LEDS_Display-((self.N_Full_Repeats)*self.Repeat_Length))
            if Patern_Current=='Repeat':
                for i in np.arange(self.N_Full_Repeats):
                    self.LED_Patern_Points[0,int(i*self.Repeat_Length):int((i+1)*self.Repeat_Length),:]=self.Function_Points[:,:,:]
                self.LED_Patern_Points[0,int(self.N_Full_Repeats*self.Repeat_Length):,:]=self.Function_Points[:,:self.Extra_Points_Needed,:]
            
            if Patern_Current=='Repeat Mirror':
                self.Repeat_Mirror_Status=False
                for i in np.arange(self.N_Full_Repeats):
                    if self.Repeat_Mirror_Status==False:
                        self.LED_Patern_Points[0,int(i*self.Repeat_Length):int((i+1)*self.Repeat_Length),:]=self.Function_Points[:,:,:]
                        self.Repeat_Mirror_Status=True
                            
                    elif self.Repeat_Mirror_Status==True:
                        self.LED_Patern_Points[0,int(i*self.Repeat_Length):int((i+1)*self.Repeat_Length),:]=np.fliplr(self.Function_Points[:,:,:])
                        self.Repeat_Mirror_Status=False
                        
                if self.Repeat_Mirror_Status==False:
                    self.LED_Patern_Points[0,int(self.N_Full_Repeats*self.Repeat_Length):,:]=self.Function_Points[:,:self.Extra_Points_Needed,:]
                    
                elif self.Repeat_Mirror_Status==True:
                    self.LED_Patern_Points[0,int(self.N_Full_Repeats*self.Repeat_Length):,:]=np.fliplr(self.Function_Points[:,(self.Repeat_Length-self.Extra_Points_Needed):,:])
            
        LED_Patern_Points_Old=self.LED_Patern_Points #mostly for banger 
        
        self.LED_Patern_Points=self.LED_Patern_Points*self.Master_Brightness #scale RGB by master brightness
        
        
        
        self.LED_Mirror_Points = np.zeros(np.shape(self.LED_Patern_Points))
        if Mirror_Current == 'No Mirror':
            self.LED_Mirror_Points = self.LED_Patern_Points
        if Mirror_Current == 'Full Mirror':
            self.LED_Mirror_Points[:,:,:]=np.fliplr(self.LED_Patern_Points[:,:,:])
        if Mirror_Current == 'L to R':
            self.LED_Mirror_Points = self.LED_Patern_Points
            self.LED_Mirror_Points[:,:int(N_LEDS_Display/2),:]=np.fliplr(self.LED_Patern_Points[:,int(N_LEDS_Display/2):,:])
        if Mirror_Current == 'R to L':
            self.LED_Mirror_Points = self.LED_Patern_Points
            self.LED_Mirror_Points[:,int(N_LEDS_Display/2):,:]=np.fliplr(self.LED_Patern_Points[:,:int(N_LEDS_Display/2),:])
            
        
        K107A=False      # for K-107
        if K107A:
            self.LED_Patern_Points_Physical = LED_Physical_Strip.Main_Func("K107A", self.LED_Mirror_Points, None)
        Circle=True
        if Circle:
            self.LED_Patern_Points_Physical = LED_Physical_Strip.Main_Func("Full Circle", self.LED_Mirror_Points, None)
        
        self.LED_Mirror_Points = self.LED_Patern_Points_Physical.Out
            
        
        self.Data_To_Send=np.uint8(np.zeros(np.size(self.LED_Mirror_Points,1)*3))
        for i in np.arange(np.size(self.LED_Mirror_Points,1)):
            self.Data_To_Send[i*3:i*3+3]=np.round(self.LED_Mirror_Points[0,i,:].transpose(0)*255)
        
        Debug_LED = False
        if Debug_LED:
            if self.Func_Frame%2==0:
                self.Data_To_Send[0]=100
                self.Data_To_Send[1]=0
                self.Data_To_Send[2]=0
                self.Data_To_Send[3]=0
                self.Data_To_Send[4]=0
                self.Data_To_Send[5]=0
            else:
                self.Data_To_Send[0]=0
                self.Data_To_Send[1]=0
                self.Data_To_Send[2]=0
                self.Data_To_Send[3]=100
                self.Data_To_Send[4]=0
                self.Data_To_Send[5]=0
        
        self.Extra_Data=np.uint8(np.zeros(8))
        #0 Quit Stream (Keep Server Up)
        #1 Quit Server
        #2
        #3
        #4
        #5
        #6
        #7
        #8
        
        if Quit_State=='Quit Stream':            
            self.Extra_Data[0]=1
        
        if Quit_State=='Quit Server':
            self.Extra_Data[1]=1
            
        #self.Data_To_Send[:] = 100
            
        self.Data_To_Send=np.append(self.Data_To_Send,self.Extra_Data)
        
        
        
        if Quit_State=='Quit Stream' or Quit_State=='Quit Server':
            w.close()
            clientSocket.close()
            #breakpoint()
            global t
            t.stop()
        else:
            Send_Success=send(self.Data_To_Send, clientSocket)
            if Send_Success==False:
                w.Music.Press_Button('Quit Stream')

            
        
t = QtCore.QTimer()
t.timeout.connect(Main_Func)

t.start(1)

if Quit_State=='Quit Stream' or Quit_State=='Quit Server':
    t.stop()
    
app.exec()
#breakpoint()
sys.exit(0)