
#Source: http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html
import os
if os.name == "posix":
    import smbus
import time
import math

class Compass(object):
    
    def __init__(self):
        
        if os.name == "posix":
            self.bus = smbus.SMBus(1)
            self.address = 0x1e
            self.scale = 0.92
            
            self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
            self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
            self.write_byte(2, 0b00000000) # Continuous sampling
            self.bearing = 0
        else:
            print "Compass cannot be initialized on non-raspberrypi OS!"

    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)
    
    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val
    
    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    
    def write_byte(self,adr,value):
        self.bus.write_byte_data(self.address, adr, value)
        
    def readX(self):
        return self.read_word_2c(3) * self.scale
    
    def readY(self):
        return self.read_word_2c(7) * self.scale
        
    def readZ(self):
        return self.read_word_2c(5) * self.scale
        
    def getBearing(self):
        self.x_out = self.readX()
        self.y_out = self.readY()
        tempBearing  = math.atan2(self.y_out, self.x_out) 
        if (tempBearing < 0):
            tempBearing += 2 * math.pi

        self.bearing = math.degrees(tempBearing)
        return self.bearing
