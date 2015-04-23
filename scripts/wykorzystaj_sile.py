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



if __name__ == '__main__':


	
	rospy.Subscriber("pnp", Float32MultiArray, callbackPnp)

	irpos = IRPOS("wyswietl_punkty", "Irp6ot", 7, "irp6ot_manager")
	


	world_points = []
	
	irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.4), Quaternion(0.0, 0.0, 0.0, 1.0)))

	

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

		

	while not rospy.is_shutdown():
		
		#punkt w ukladzie kartki
		point = numpy.matrix([[0.0],[0.0],[0.0],[1]])	
							

		#punkt w ukladzie optical frame
		#point = current_matrix * point

		#punkt w ukladzie kamery
		optical_to_camera = numpy.matrix([[-1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]])
		#point = optical_to_camera * point

		#punkt w ukladzie narzedzia (40cm ponizej tl6: 40cm - 13cm = 27cm)
		camera_to_tl6 = numpy.matrix([[0,-1,0,-0.0551],[1,0,0,0],[0,0,1,0.13],[0,0,0,1]])
		#camera_to_tl6 = inverse_matrix(camera_to_tl6)
		#point = camera_to_tl6*point
		#
						

		#punkt w ukladzie swiata
		TBG = quaternion_matrix(quaternion)
		TBG = TBG + numpy.matrix([[0,0,0,pX],[0,0,0,pY],[0,0,0,pZ],[0,0,0,0]])

		
		#point = TBG * camera_to_tl6 * optical_to_camera * current_matrix * point
		#point = TBG * camera_to_tl6 * optical_to_camera * current_matrix * point
			
		current_matrix[1,3] = current_matrix[1,3]+0.01	
		point = TBG * camera_to_tl6  * optical_to_camera * current_matrix * point

						
						
		print "%.5f" % point[0]
		print "%.10f" % point[1]
		print "%.5f" % point[2]
		print "%.5f" % point[3]
		print"******"
		
		
		




		rospy.sleep(1.0)



















		
	
	
