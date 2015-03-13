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



point0 = numpy.matrix('0;0;0;1')
point1 = numpy.matrix('0.21;0;0;1')
point2 = numpy.matrix('0;0.297;0;1')
point3 = numpy.matrix('0.21;0.297;0;1')

topic = 'visualization_marker_array'
publisher = rospy.Publisher(topic, Marker)




def callback(data):
	global lastData
	dataLock.acquire()
	lastData = data.data
	dataLock.release()
    
#def calculatePoint():
	


if __name__ == '__main__':

	
	rospy.Subscriber("pnp", Float32MultiArray, callback)
	irpos = IRPOS("publikowanie_rogu", "Irp6ot", 7, "irp6ot_manager")
	
	global move
	move = move_track(irpos)
	
	
	global matrix
	for i in range(1, 2):
	#	calculatePosition()
		
		if lastData:
			for j in range(0,3):
				for k in range(0,4):
					matrix[j,k] = lastData[j*4+k]
					
			
		#rospy.sleep(3)
		
	point0 = matrix * point0
	point1 = matrix * point1
	point2 = matrix * point2
	point3 = matrix * point3
	
	print lastData
	print matrix
	
	print point0
	print point1
	print point2
	print point3
	
	print point0[0]
	print point0[1]
	print point0[2]
	print point0[3]
	
	
	while not rospy.is_shutdown():
	
		marker = Marker()
		marker.header.frame_id = "/t_c_optical_frame"
		marker.type = marker.POINTS
		marker.action = marker.ADD
		marker.scale.x = 0.01
		marker.scale.y = 0.01
		marker.color.a = 1.0
		marker.color.g = 1.0
		marker.pose.orientation.w = 1.0
		p = Point()
		p.x = point0[0]
		p.y = point0[1]
		p.z = point0[2]
		marker.points.append(p)
		
		
		
		
		p1 = Point()
		p1.x = point1[0]
		p1.y = point1[1]
		p1.z = point1[2]
		marker.points.append(p1)
		
		
		
		
		p2 = Point()
		p2.x = point2[0]
		p2.y = point2[1]
		p2.z = point2[2]
		marker.points.append(p2)
		
		
		
		
		p3 = Point()
		p3.x = point3[0]
		p3.y = point3[1]
		p3.z = point3[2]
		marker.points.append(p3)
		
		
		publisher.publish(marker)
		
		
		
		rospy.sleep(0.01)
		
	
	
	
	

	print "OK"
	
	
	
	
	
	
	
