import time
import numpy
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np

file1 = "data/sensor_values.npy"
file2 = "data/frontLegSensorValues.npy"
num_iterations = 1000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(num_iterations)
frontLegSensorValues = np.zeros(num_iterations)

for i in range(0,num_iterations):
    p.stepSimulation()
    backLegSensorValues[i]  = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    #print(backLegSensorValues[i])

    time.sleep(1/60)
# end for i 
p.disconnect()
# Saving sensor values to numpy files in "data" subdirectory
np.save(file1, backLegSensorValues)
np.save(file2, frontLegSensorValues)