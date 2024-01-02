import numpy as np

class Main_Func():
    def __init__(self, Arangement, LED_Patern_Points, parent=None):
        super(Main_Func, self).__init__()  
        self.Arangement=Arangement
        self.LED_Patern_Points=LED_Patern_Points
        if Arangement == 'Full Circle':
            self.Out=np.zeros((1, 600, 3))
            self.Out[:,:,:]=self.LED_Patern_Points[:,:,:]
        
        if Arangement == 'K107A':
            self.Out=np.zeros((1, 600, 3))
            for i in np.arange(600):
                # if i>=0 and i<=140:
                if i>=0 and i<=149:
                    self.Out[0,i,:]=self.LED_Patern_Points[0,i,:]

                #Skip LED_Patern_Points[150]    
                    
                # if i>=150 and i<=299:
                if i>=150 and i<=299:
                    self.Out[0,i,:]=self.LED_Patern_Points[0,i+1,:]
                # if i>=300 and i<=449:
                if i>=300 and i<=449:
                    self.Out[0,i,:]=self.LED_Patern_Points[0,443-(i-300),:]
                    
                #skip LED_Patern_Points[291]
                    
                # if i>=450 and i<=599:
                if i>=450 and i<=599:
                    self.Out[0,i,:]=self.LED_Patern_Points[0,443-(i-300)-1,:]
                
                # LED_Patern_Points     |   0-143   |  144-149  |    150    |  151-293  |    294    |  295-300  |  301-444  |
                # Strip 1               |   0-143   |  144-149  |     X     |  150-292  |    293    |  294-299  |   
                # Strip 2               |           |  599-594  |    593    |  592-450  |     X     |  449-444  |  443-300  |