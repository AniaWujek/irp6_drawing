#!/usr/bin/env python
from irpos import *

from move_track import *
from punkt import *
import math
import threading
from std_msgs.msg import *
from transformations import *
from numpy import *
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray


dataLockPoints = threading.Lock()
dataLockPnp = threading.Lock()

points = None
lastData = None

matrix = numpy.zeros(shape=(4,4))
matrix[3,3] = 1.0

def callbackPnp(data):

	global matrix
	dataLockPnp.acquire()
	lastData = data.data
	for j in range(0,3):
		for k in range(0,4):
			matrix[j,k] = lastData[j*4+k]
	dataLockPnp.release()

def checkPoint(point):
	if (point[0] < 0.65) or (point[0] > 1.0) or (point[1] < -0.25) or (point[1] > 0.90) :
		print "point error!"
		print point
		return False
	else:
		return True

if __name__ == '__main__':


	
	rospy.Subscriber("pnp", Float32MultiArray, callbackPnp)

	irpos = IRPOS("stuknij_rogi", "Irp6ot", 7, "irp6ot_manager")
	move = move_track(irpos)

	world_points = []
	
	irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))

	print "czekaj ..."
	rospy.sleep(1.0)
	print "... wyczekane!"
	
	
	cartPosition = irpos.get_cartesian_pose()

	qX = cartPosition.orientation.x
	qY = cartPosition.orientation.y
	qZ = cartPosition.orientation.z
	qW = cartPosition.orientation.w

	pX = cartPosition.position.x
	pY = cartPosition.position.y
	pZ = cartPosition.position.z

	quaternion = [qX, qY, qZ, qW]

	current_matrix = matrix

		

	
		
	#punkt w ukladzie kartki
	p0 = numpy.matrix([[0.105],[0.148],[0.0],[1]])		

	#punkt w ukladzie kamery
	optical_to_camera = numpy.matrix([[-1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]])		

	#punkt w ukladzie narzedzia (40cm ponizej tl6: 40cm - 13cm = 27cm)
	camera_to_tl6 = numpy.matrix([[0,-1,0,-0.0551],[1,0,0,0],[0,0,1,0.13],[0,0,0,1]])								

	#punkt w ukladzie swiata
	TBG = quaternion_matrix(quaternion)
	TBG = TBG + numpy.matrix([[0,0,0,pX],[0,0,0,pY],[0,0,0,pZ],[0,0,0,0]])
	
	#current_matrix[1,3] = current_matrix[1,3] - 0.01
	current_matrix[0,3] = current_matrix[0,3] - 0.02	
		
	p0 = TBG * camera_to_tl6  * optical_to_camera * current_matrix * p0
	

						
	if checkPoint(p0):
		print "p0 ok"
	
		
	if 	checkPoint(p0):		
		
		
		irpos.move_to_cartesian_pose(8.0, Pose(Point(p0[0], p0[1], irpos.get_cartesian_pose().position.z), irpos.get_cartesian_pose().orientation))		
		



















		
	
	
