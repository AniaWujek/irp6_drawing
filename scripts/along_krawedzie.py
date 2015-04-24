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

licznik = 0

matrix = numpy.zeros(shape=(4,4))
matrix[3,3] = 1.0



def callbackPnp(data):

	global matrix
	global licznik
	dataLockPnp.acquire()
	lastData = data.data
	for j in range(0,3):
		for k in range(0,4):
			matrix[j,k] = lastData[j*4+k]
	licznik = licznik + 1
	dataLockPnp.release()

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

def checkPoint(point):
	if (point[0] < 0.65) or (point[0] > 1.0) or (point[1] < -0.25) or (point[1] > 0.90) or (point[2] < 1.35) or (point[2] > 1.60):
		print "point error!"
		print point
		return False
	else:
		return True

if __name__ == '__main__':


	
	
	rospy.Subscriber("pnp", Float32MultiArray, callbackPnp)
	rospy.Subscriber("points", Float32MultiArray, callbackPoints)

	#irpos = IRPOS("stuknij_rogi", "Irp6ot", 7, "irp6ot_manager")
	irpos = IRPOS("stuknij_rogi", "Irp6ot", 7)
	move = move_track(irpos)
	irpos.conmanSwitch([irpos.robot_name+'mForceTransformation'], [], True)
	


	world_points = []
	
	irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))

	print "czekaj ..."
	rospy.sleep(5.0)
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
	current_points = points
	
	#punkt w ukladzie kamery
	optical_to_camera = numpy.matrix([[-1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]])		

	#punkt w ukladzie narzedzia (40cm ponizej tl6: 40cm - 13cm = 27cm)
	camera_to_tl6 = numpy.matrix([[0,-1,0,-0.0551],[1,0,0,0],[0,0,1,0.13],[0,0,0,1]])								

	#punkt w ukladzie swiata
	TBG = quaternion_matrix(quaternion)
	TBG = TBG + numpy.matrix([[0,0,0,pX],[0,0,0,pY],[0,0,0,pZ],[0,0,0,0]])
				
	#current_matrix[1,3] = current_matrix[1,3] - 0.01
	current_matrix[0,3] = current_matrix[0,3] - 0.02

	pointsVector = []
	czas = 0.0
	oldPoint = None
	first = True
	

	
	if current_points:
		
			
		for contour in current_points:
			first = True
			pointsVector = []
			
			for i in range(0,len(contour)-1,2):					
                		
				#punkt w ukladzie kartki
				point = numpy.matrix([[contour[i]],[contour[i+1]],[0],[1]])	

					
					
				point = TBG * camera_to_tl6  * optical_to_camera * current_matrix * point
				
				point[2] = point[2] + 0.40

									
				if checkPoint(point):
					print "p0 ok"
	
					
				if 	checkPoint(point):
					
					#~  !!!!!!!!!!!!!!!! PILNOWAC CZASOW I KOLEJNOSCI !!!!!!!!!!!!!!!!	
					
					if first:
						pointCartTraj = CartesianTrajectoryPoint(rospy.Duration(5.0), Pose(Point(point[0], point[1], point[2]), irpos.get_cartesian_pose().orientation), Twist())
						pointsVector.append(pointCartTraj)
						first = False
						oldPoint = point
						
					else:
						diff = math.sqrt(abs(pow(point[0] - oldPoint[0], 2) + pow(point[1] - oldPoint[1], 2)))
						czas = czas + diff / 0.02
						print diff
						pointCartTraj = CartesianTrajectoryPoint(rospy.Duration(czas), Pose(Point(point[0], point[1], point[2]), irpos.get_cartesian_pose().orientation), Twist())									
						pointsVector.append(pointCartTraj)
						oldPoint = point
			
			#~ irpos.move_along_cartesian_trajectory(pointsVector)
								
							
					
					
					

					
									
		
		#~ irpos.move_along_cartesian_trajectory(pointsVector)
		#~ 
		#~ move.pozycjaRobocza(10.0)
		#~ irpos.move_rel_to_cartesian_pose(7.0, Pose(Point(0.1, 0.0, -0.15), Quaternion(0.0, 0.0, 0.0, 1.0)))	
		print pointsVector
		
		irpos.conmanSwitch([], [irpos.robot_name+'mForceTransformation'], True)



















		
	
	
