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


def callbackPoints(data):
	global points
	dataLockPoints.acquire()

	ind = 1
	if data.data:
		contours_number = int(data.data[0])
		points = []
		for i in range(1,contours_number):
			arraySize = int(data.data[ind])

			start = ind+1
			end = ind + arraySize*2 + 1
			points.append(data.data[start:end])
			ind = ind + arraySize*2 + 1

	dataLockPoints.release()

def callbackPnp(data):

	global matrix
	dataLockPnp.acquire()
	lastData = data.data
	for j in range(0,3):
		for k in range(0,4):
			matrix[j,k] = lastData[j*4+k]
	dataLockPnp.release()



if __name__ == '__main__':


	rospy.Subscriber("points", Float32MultiArray, callbackPoints)
	rospy.Subscriber("pnp", Float32MultiArray, callbackPnp)

	irpos = IRPOS("wyswietl_punkty", "Irp6ot", 7, "irp6ot_manager")


	world_points = []

	while not rospy.is_shutdown():

		cartPosition = irpos.get_cartesian_pose()

		qX = cartPosition.orientation.x
		qY = cartPosition.orientation.y
		qZ = cartPosition.orientation.z
		qW = cartPosition.orientation.w

		pX = cartPosition.position.x
		pY = cartPosition.position.y
		pZ = cartPosition.position.z

		quaternion = [qX, qY, qZ, qW]



		if points:
			for contour in points:
				for i in range(0,len(contour)-2,2):

                    #punkt w ukladzie kartki
					point = numpy.matrix([[contour[i]],[contour[i+1]],[0],[1]])
					#point[0] = contour[i]
					#point[1] = contour[i+1]
					
					#point[2] = 0
					#point[3] = 1
					

					#punkt w ukladzie optical frame
					point = matrix * point

					to_camera = numpy.matrix([[-1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]])

					#punkty w ukladzie kamery (tylko obrot)
					point = to_camera * point



					TBG = quaternion_matrix(quaternion)
					TBG = TBG + numpy.matrix([[0,0,0,pX],[0,0,0,pY],[0,0,0,pZ],[0,0,0,0]])

					#punkt w ukladzie swiata
					point = TBG * point
					
					print point


		rospy.sleep(1.0)


















