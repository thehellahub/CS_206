import sys
import pybullet as p
import os
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    
    def __init__(self, solutionID, GUI):
        self.directOrGUI = GUI
        self.solutionID = solutionID
        self.robotID = p.loadURDF("body.urdf")
        self.robotId = self.robotID
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain{}.nndf".format(self.solutionID))
        os.system("rm brain{}.nndf".format(self.solutionID))

    def Prepare_To_Sense(self):
        self.sensors = dict()
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Think(self):
        self.nn.Update()
        if self.directOrGUI != 'DIRECT':
            self.nn.Print()

    def Prepare_To_Act(self):
        self.motors = dict()
        for jointName in pyrosim.jointNamesToIndices:
            jointName = jointName.decode('ASCII')
            #print(f"Joint name is: {jointName}")
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, index):
        for linkName in self.sensors:
            SENSOR.Get_Value(self.sensors[linkName], index)

    def Act(self, index):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                MOTOR.Set_Value(self.motors[jointName], desiredAngle, self.robotId)
                #print(f"\nNeuron name is: {neuronName}, joint name is: {jointName}, \
                #        desired angle is: {desiredAngle}")


    def Get_Fitness(self, solutionID):
        self.stateOfLinkZero = p.getLinkState(self.robotID,0)
        positionOfLinkZero = self.stateOfLinkZero[0]

        xCoordinateOfLinkZero = positionOfLinkZero[0]

        with open('tmp{}.txt'.format(solutionID), 'w') as f:
            f.write(str(xCoordinateOfLinkZero))

        os.rename("tmp"+str(solutionID)+".txt" , "fitness"+str(solutionID)+".txt")