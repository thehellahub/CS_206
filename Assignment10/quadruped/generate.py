import pyrosim.pyrosim as pyrosim
import random

def Create_World():

    pyrosim.Start_SDF("world.sdf")

    x = 10
    y = 10
    z = 0.5

    pyrosim.Send_Cube(name=f"Box", pos=[x,y,z] , size=[1,1,1])
    
    pyrosim.End()

def Create_Arch():

    pyrosim.Start_URDF("body.urdf")

    length = 1
    width  = 1
    height = 1
                                                #    x,y,z
    pyrosim.Send_Cube(  name =f"Link0",         pos=[0,0,0.5] ,     size=[length,width,height])
    pyrosim.Send_Joint( name =f"Link0_Link1" ,  parent= "Link0" ,   child = "Link1" , type = "revolute", position = [0,0,1])
    pyrosim.Send_Cube(  name =f"Link1",         pos=[0,0,0.5] ,     size=[length,width,height])
    pyrosim.Send_Joint( name =f"Link1_Link2" ,  parent= "Link1" ,   child = "Link2" , type = "revolute", position = [0,0,1])
    pyrosim.Send_Cube(  name =f"Link2",         pos=[0,0,0.5] ,     size=[length,width,height])
    pyrosim.Send_Joint( name =f"Link2_Link3" ,  parent= "Link2" ,   child = "Link3" , type = "revolute", position = [0,0.5,0.5])
    pyrosim.Send_Cube(  name =f"Link3",         pos=[0,0.5,0] ,     size=[length,width,height])
    pyrosim.Send_Joint( name =f"Link3_Link4" ,  parent= "Link3" ,   child = "Link4" , type = "revolute", position = [0,1,0])
    pyrosim.Send_Cube(  name =f"Link4",         pos=[0,0.5,0] ,     size=[length,width,height])
    pyrosim.Send_Joint( name =f"Link4_Link5" ,  parent= "Link4" ,   child = "Link5" , type = "revolute", position = [0,0.5,-0.5])
    pyrosim.Send_Cube(  name =f"Link5",         pos=[0,0,-0.5] ,    size=[length,width,height])
    pyrosim.Send_Joint( name =f"Link5_Link6" ,  parent= "Link5" ,   child = "Link6" , type = "revolute", position = [0,0,-1])
    pyrosim.Send_Cube(  name =f"Link6",         pos=[0,0,-0.5] ,    size=[length,width,height])

    pyrosim.End()

### WITH BACK LEG AS ROOT (LOOKS CORRECT?)
def Create_Robot():
    x, y, z                 = .5, .5, .5
    length, width, height   =  1,  1,  1

    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube( name="BackLeg", pos=[x, y, z], size=[length, width, height])
    pyrosim.Send_Joint(name="BackLeg_Torso", parent="BackLeg", child="Torso", type="revolute", position=[1, 0, 1])
    pyrosim.Send_Cube( name="Torso", pos=[.5, .5, .5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[1,.5,0])
    pyrosim.Send_Cube( name="FrontLeg", pos=[.5, 0, -.5], size=[length, width, height])

    pyrosim.End()

def Generate_Body():
    length, width, height   =  1,  1,  1

    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube( name="Torso", pos=[1, 0, 1.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0.5, 0, 1])
    pyrosim.Send_Cube( name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[1.5,0,1])
    pyrosim.Send_Cube( name="FrontLeg", pos=[.5, 0, -.5], size=[length, width, height])

    pyrosim.End()

def Generate_Brain(id):
    pyrosim.Start_NeuralNetwork(f"brain{id}.nndf")

    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

    pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

    for sensor_neuron in [0,1,2]:
        for motor_neuron in [3,4]:
            pyrosim.Send_Synapse(sourceNeuronName=sensor_neuron, \
                                 targetNeuronName=motor_neuron, \
                                 weight=random.uniform(-1,1)
                                )
    pyrosim.End()

Create_World()
Generate_Body()
Generate_Brain()

