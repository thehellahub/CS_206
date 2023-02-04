import math
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p
import constants as c

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        
        #print(f"\n\nFOO: {self.jointName}")

        self.motorValues    = np.linspace(0, 2*math.pi, c.ITERATIONS)
        

        if self.jointName == b"BackLeg_Torso":
            self.amplitude      = c.AMPLITUDE_BACK_LEG
            self.frequency      = c.FREQUENCY_BACK_LEG
            self.offset         = c.PHASE_OFFSET_BACK_LEG
            self.direction      = -1
        else:
            self.amplitude      = c.AMPLITUDE_FRONT_LEG
            self.frequency      = c.FREQUENCY_FRONT_LEG
            self.offset         = c.PHASE_OFFSET_FRONT_LEG
            self.direction      = 1
            self.frequency      = self.frequency / 2 # HALF THE FREQUENCY FOR FRONT LEG

    def Set_Value(self, index, robotId):

        self.motorValues[index] = self.amplitude            *  \
                                  np.sin(self.frequency     *  \
                                    self.motorValues[index] +  \
                                    self.offset
                                  )

        pyrosim.Set_Motor_For_Joint(
            bodyIndex       = robotId,
            jointName       = self.jointName,
            controlMode     = p.POSITION_CONTROL,
            targetPosition  = self.direction * self.motorValues[index],
            maxForce        = c.MOTOR_STRENGTH
        )

        # if index == c.ITERATIONS-1:
        #     print(self.motorValues)


    def Save_Values(self):
        np.save(c.MOTOR_STRENGTH, self.motorValues)
