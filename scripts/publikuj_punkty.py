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


dataLock = threading.Lock()

move = None
lastData = None
matrix = numpy.zeros(shape=(4,4))
matrix[3,3] = 1.0
colorA = 1.0
colorR = 0.0
colorG = 1.0
colorB = 0.0

pointsMatrix = 4*[0]


pointsMatrix[0] = numpy.matrix([[0], [0], [0], [1]])
pointsMatrix[1] = numpy.matrix([[0.21], [0], [0], [1]])
pointsMatrix[2] = numpy.matrix([[0], [0.297], [0], [1]])
pointsMatrix[3] = numpy.matrix([[0.21], [0.297], [0], [1]])

topic = 'visualization_marker_array'
publisher = rospy.Publisher(topic, Marker)




def callback(data):
	global lastData
	global matrix
	global colorA
	global colorG
	dataLock.acquire()
	lastData = data.data
	colorA = 1.0
	colorG = 1.0
	for j in range(0,3):
		for k in range(0,4):
			matrix[j,k] = lastData[j*4+k]
	dataLock.release()

if __name__ == '__main__':

	
	rospy.Subscriber("pnp", Float32MultiArray, callback)
	irpos = IRPOS("publikowanie_rogu", "Irp6ot", 7, "irp6ot_manager")
	
	global move
	global colorA
	global colorG
	move = move_track(irpos)
	
	
	firstRound = True
		
	
	licznik = 0
	
	
	
	while not rospy.is_shutdown():
		
		
		
	

					
			
		
		
		point0 = matrix * pointsMatrix[0]
		point1 = matrix * pointsMatrix[1]
		point2 = matrix * pointsMatrix[2]
		point3 = matrix * pointsMatrix[3]
		
		p = Point()
		p.x = point0[0]
		p.y = point0[1]
		p.z = point0[2]		
		
		p1 = Point()
		p1.x = point1[0]
		p1.y = point1[1]
		p1.z = point1[2]
		
		p2 = Point()
		p2.x = point2[0]
		p2.y = point2[1]
		p2.z = point2[2]
		
		p3 = Point()
		p3.x = point3[0]
		p3.y = point3[1]
		p3.z = point3[2]

	
		marker = Marker()
		marker.header.frame_id = "/t_c_optical_frame"
		marker.type = marker.TRIANGLE_LIST
		marker.action = marker.ADD
		marker.scale.x = 1.0
		marker.scale.y = 1.0
		marker.scale.z = 1.0
		
		if firstRound:
			marker.color.g = 1.0
			marker.color.a = 1.0
			firstRound = False
			
		
		
		marker.color.g = colorG
		marker.color.a = colorA
		
		if colorG > 0.0:
			colorG = colorG - 0.05
		if colorG < 0.5:
			colorG = 0.0
			
			
		
		
		
		marker.points.append(p)
		marker.points.append(p1)
		marker.points.append(p2)
		marker.points.append(p3)
		marker.points.append(p2)
		marker.points.append(p1)

		
		
		publisher.publish(marker)
		

		
		
		
		rospy.sleep(0.1)
		
	
	
	
	

	print "OK"
	
	
	
	
	
	
	
