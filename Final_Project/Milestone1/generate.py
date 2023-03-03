import pyrosim.pyrosim as pyrosim
import constants as c

def Create_World():

    pyrosim.Start_SDF("world.sdf")

    length = 1
    width  = 1
    height = 1

    x = 10
    y = 10
    z = 0.5

    pyrosim.Send_Cube(name=f"Box", pos=[x,y,z] , size=[length,width,height])

    pyrosim.End()

def Create_Body():

    pyrosim.Start_URDF("body.urdf")

    foot_height     = 0.2
    shin_height     = 2.5
    thigh_height    = 2
    torso_height    = 3
    head_height     = 0.65

    torso_width     = 2
    foot_length     = 1.25
    shoulder_width  = 0.2
    shoulder_height = 0.4
    arm_width       = 0.5
    arm_height      = 2

    # Head
    head_position   = 0.43 + foot_height + shin_height + thigh_height + torso_height + head_height
    
    pyrosim.Send_Cube(name="Head",  pos=[0, 0, head_position], size=[1, 1, head_height])
    
    # Neck
    pyrosim.Send_Joint(name="Head_Neck", parent="Head", child="Neck", type="revolute",\
                       position=[0, 0, head_position-(head_height*0.5)], jointAxis="0 0 1")
    pyrosim.Send_Cube(name="Neck",  pos=[0, 0, -0.25], size=[0.65, .65, .5])
    
    # Torso

    pyrosim.Send_Joint(name="Neck_Torso", parent="Neck", child="Torso", type="revolute",\
                       position=[0, 0, -0.5], jointAxis="1 0 0")
    
    
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, ((-1)*torso_height)*.5], size=[.75, torso_width, torso_height])

    # Hip
    pyrosim.Send_Joint(name="Torso_Hip", parent="Torso", child="Hip", type="revolute",\
                       position=[0, 0, (torso_height)*-1], jointAxis="0 1 0") # rotates with 0 0 1
    pyrosim.Send_Cube(name="Hip", pos=[0, 0, -0.125],   size=[.75, 2, 0.25])
    

    """  LOWER BODY   """

    # Thighs

    
    pyrosim.Send_Joint(name="Hip_UpperLleg", parent="Hip", child="UpperLleg", type="revolute",
                       position=[0,-0.625,-0.25], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="UpperLleg", pos=[0, 0, (-1)*(thigh_height/2)], size=[0.65, 0.65, thigh_height])

    pyrosim.Send_Joint(name="Hip_UpperRleg", parent="Hip", child="UpperRleg", type="revolute",
                       position=[0,0.625,-0.25], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="UpperRleg", pos=[0, 0, (-1)*(thigh_height/2)], size=[0.65, 0.65, thigh_height])


    # ''' Lower legs '''


    pyrosim.Send_Joint(name="UpperLleg_LowerLleg", parent="UpperLleg", child="LowerLleg", type="revolute",
                       position=[0, 0, -1*(thigh_height)], jointAxis="0 1 0")
    
    pyrosim.Send_Cube(name="LowerLleg", pos=[0, 0, (-1)*(shin_height/2)], size=[.5, .5, shin_height])

    pyrosim.Send_Joint(name="UpperRleg_LowerRleg", parent="UpperRleg", child="LowerRleg", type="revolute",
                       position=[0, 0, -1*(thigh_height)], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="LowerRleg", pos=[0, 0, (-1)*(shin_height/2)], size=[.5, .5, shin_height])


    # # Feet

    pyrosim.Send_Joint(name="LowerLleg_LFoot", parent="LowerLleg", child="LFoot", type="revolute",
                       position=[.15, 0, (-1)*shin_height], jointAxis="0 1 0")

    
    pyrosim.Send_Cube(name="LFoot", pos=[(foot_length/4)-(foot_length/8),0,(-1)*(foot_height/2)], size=[foot_length,.4,foot_height])

    pyrosim.Send_Joint(name="LowerRleg_RFoot", parent="LowerRleg", child="RFoot", type="revolute",
                       position=[.15, 0, (-1)*shin_height], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="RFoot", pos=[(foot_length/4)-(foot_length/8),0,(-1)*(foot_height/2)], size=[foot_length,.4,foot_height])



    # """ UPPER BODY  """

    # # Shoulders and arms
    # #
    if c.ARMS:
        pyrosim.Send_Joint(name="Torso_Lshoulder", parent="Torso", child="Lshoulder", type="revolute",
                           position=[0,(-1)*(torso_width/2),-.25], jointAxis="1 1 0")

        
        pyrosim.Send_Cube(name="Lshoulder", pos=[0, (-1)*(shoulder_width/2), 0], size=[.5, shoulder_width, shoulder_height])


        pyrosim.Send_Joint(name="Torso_Rshoulder", parent="Torso", child="Rshoulder", type="revolute",
                           position=[0,(torso_width/2),-.25], jointAxis="1 1 0")

        pyrosim.Send_Cube(name="Rshoulder", pos=[0, (shoulder_width/2), 0], size=[.5, shoulder_width, shoulder_height])


        # # Arms
        
        pyrosim.Send_Joint(name="Lshoulder_LUpperArm", parent="Lshoulder", child="LUpperArm", type="revolute",
                           position=[0, (-1)*shoulder_width, 0], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LUpperArm", pos=[0, (-1)*(arm_width/2), ((-1)*(arm_height/2))], size=[.2, arm_width, arm_height])

        pyrosim.Send_Joint(name="LUpperArm_LLowerArm", parent="LUpperArm", child="LLowerArm", type="revolute",
                           position=[0, (-1)*(arm_width/2), (-1)*(arm_height)], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LLowerArm", pos=[0, 0, (-1)*(arm_height/2)], size=[.25, arm_width, arm_height])


        pyrosim.Send_Joint(name="Rshoulder_RUpperArm", parent="Rshoulder", child="RUpperArm", type="revolute",
                           position=[0, shoulder_width, 0], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RUpperArm", pos=[0, (arm_width/2), ((-1)*(arm_height/2))], size=[.2, arm_width, arm_height])

        pyrosim.Send_Joint(name="RUpperArm_RLowerArm", parent="RUpperArm", child="RLowerArm", type="revolute",
                           position=[0, (arm_width/2), (-1)*(arm_height)], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RLowerArm", pos=[0, 0, (-1)*(arm_height/2)], size=[.25, arm_width, arm_height])

        pyrosim.End()

Create_World()
Create_Body()


