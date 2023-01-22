import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length = 1
width  = 1
height = 1
x = 0
y = 0
z = 0.5
for g in range(0,5):
	for h in range(0,5):
		for i in range(0,10):
			pyrosim.Send_Cube(name=f"Box{i}", pos=[x,y,z] , size=[length,width,height])
			z += 1
			length = length * 0.9
			width  = width 	* 0.9
			height = height * 0.9
		# end for i
		length = 1
		width  = 1
		height = 1
		x += 1
		z =  0.5
	# end for h	
	x =  0
	y += 1
	z =  0.5	
# end for g 
pyrosim.End()

