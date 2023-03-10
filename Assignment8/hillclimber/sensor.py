import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:
    
    def __init__(self, linkName):
        self.linkName = linkName
        self.Prepare_To_Sense()

    def Prepare_To_Sense(self):
        self.values = np.zeros(c.ITERATIONS)

    def Get_Value(self, index):
        self.values[index] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        np.save(c.SENSOR_VALUES, self.values)