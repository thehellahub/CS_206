import time
import pybullet_data
import pybullet as p
import constants as c
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT


class SIMULATION:

    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):

        for i in range(c.ITERATIONS):
            #print(i)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            time.sleep(1 / 120)

    def __del__(self):
        p.disconnect()