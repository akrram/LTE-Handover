import math

class Location:#location in a grid 500 miles x 500 miles [not enforcing the limits]
    def __init__(self, x, y):
        self.coordinate = (x,y)
    def __str__(self):
        return str(self.coordinate)
    def __getitem__(self, index):
        return self.coordinate[index]
    def __str__ (self):
        str1 = str(self.coordinate)
        return str1   
        
class eNB: 
    def __init__(self, location, SRRI, noise):      
        self.location = location
        self.SRRI = SRRI#dB
        self.noise = noise#dB
        self.SNR = self.SRRI-self.noise#SNR in dB
        
    def __str__ (self):
        str1 = "Location: "+str(self.location)+" SRRI: "+str(self.SRRI)+ " dB   Noise:"+ str(self.noise)+" dB"
        return str1
    
    
class UE:
    def __init__(self, location, final_location, speed ):
        self.location = location
        self.final_location = final_location
        self.speed = speed
        
    def __str__ (self):
        str1 = "Initial Location: "+str(self.location)+" final_location: "+str(self.final_location)+ " Speed:"+ str(self.speed)+" MPH"
        return str1