import time
import math
import numpy
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

iterations      = 1000
motor_strength  = 15

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
pyrosim.Prepare_To_Simulate(robotId)

amplitude_BackLeg       = math.pi/4
frequency_BackLeg       = 8
phaseOffset_BackLeg     = 5
backLegSensorValues     = numpy.zeros(iterations)
targetAngles_BackLeg    = np.linspace(0, 2*math.pi, iterations)

amplitude_FrontLeg      = math.pi/4
frequency_FrontLeg      = 125
phaseOffset_FrontLeg    = math.pi/4
frontLegSensorValues    = numpy.zeros(iterations)
targetAngles_FrontLeg   = np.linspace(0, 2*math.pi, iterations)

for i in range(0, iterations):
    targetAngles_BackLeg[i]  = amplitude_BackLeg  * np.sin(frequency_BackLeg  * targetAngles_BackLeg[i]  + phaseOffset_BackLeg)
    targetAngles_FrontLeg[i] = amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_FrontLeg[i] + phaseOffset_FrontLeg)
# end for i

for i in range(0, iterations):
    p.stepSimulation()
    backLegSensorValues[i]  = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b"BackLeg_Torso",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_BackLeg[i],
        maxForce=motor_strength)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b"Torso_FrontLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_FrontLeg[i]*-1,
        maxForce=motor_strength)
    time.sleep(1/60) 
# end for i

file1 = "data/sensor_values.npy"
file2 = "data/frontLegSensorValues.npy"
file3 = "data/targetValues_BackLeg.npy"
file4 = "data/targetValues_FrontLeg.npy"

p.disconnect()
np.save(file1, backLegSensorValues)
np.save(file2, frontLegSensorValues)
np.save(file3, targetAngles_BackLeg)
np.save(file4, targetAngles_FrontLeg)