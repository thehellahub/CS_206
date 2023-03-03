import time

import numpy

import pyrosim.pyrosim as pyrosim
import constants as c
from constants import*
import random
import os
import sys

length = 1
width = 1
height = 1

class SOLUTION:

    def __init__(self, myID):
        self.myID = myID
        self.weights = numpy.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS)
        self.weights = self.weights * 2 - 1

        # self.weights * 2 - 1

    # def Evaluate(self, GUI):
    #     self.Create_World()
    #     self.Create_Body()
    #     self.Create_Brain()
    #     os.system("python simulate.py {} {}".format(GUI, self.myID))
    #     while not os.path.exists('fitness{}.txt'.format(self.myID)):
    #         time.sleep(0.01)
    #     with open('fitness{}.txt'.format(self.myID), 'r') as f:
    #         result = f.readline()
    #         result = float(result)
    #     self.fitness = result

    def Start_Simulation(self, GUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python simulate.py {} {} 2&>1 &".format(GUI, self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('fitness{}.txt'.format(self.myID)):
            time.sleep(0.01)
        # while not os.access('fitness{}.txt'.format(self.myID), os.R_OK):
        #     time.sleep(0.01)
        try:
            with open('fitness{}.txt'.format(self.myID), 'r') as f:
                result = f.readline()
                result = float(result)
        except Exception as e:
            print(e)
        self.fitness = result
        #print("\n\nFitness of ID: {}, = {}".format(self.myID, self.fitness))
        os.system("rm fitness{}.txt".format(self.myID))

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="T", pos=[x-2, y-2, z], size=[length, width, height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[length, width, height])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, 0.5, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2,1,0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -0.5, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2,1,0.2])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube( name="LeftLeg",  pos=[-.5, 0, 0],    size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube( name="RightLeg", pos=[.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg",   parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0, 1, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube( name="FrontLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg",     parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0, -1, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube( name="BackLowerLeg",  pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg",   parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube( name="RightLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg",     parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube( name="LeftLowerLeg",  pos=[0, 0, -.5], size=[0.2, 0.2, 1])

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain{}.nndf".format(self.myID))
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")

        pyrosim.Send_Motor_Neuron(name=9, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=13, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")

        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()


    def Mutate(self):

        randRow = random.randint(0, 2)

        randColumn = random.randint(0, 1)

        self.weights[randRow][randColumn] = random.random() * 2 - 1


    def Set_ID(self, ID):
        self.myID = ID
