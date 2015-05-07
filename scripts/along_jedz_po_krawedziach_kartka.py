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
		for i in range(0,contours_number):
			arraySize = int(data.data[ind])

			start = ind+1
			end = ind + arraySize*2 + 1
			points.append(data.data[start:end])
			ind = ind + arraySize*2 + 1

	#~ print contours_number, len(points)


	dataLockPoints.release()

def checkPoint(point):
	if (point[0] < 0.65) or (point[0] > 1.0) or (point[1] < 0.05) or (point[1] > 0.55) or (point[2] < 1.35) or (point[2] > 1.60):
		print "point error!"
		print point
		return False
	else:
		return True

if __name__ == '__main__':


	
	
	rospy.Subscriber("pnp", Float32MultiArray, callbackPnp)
	rospy.Subscriber("points", Float32MultiArray, callbackPoints)

	irpos = IRPOS("jedz_krawedzie", "Irp6ot", 7, "irp6ot_manager")
	#irpos = IRPOS("jedz_krawedzie", "Irp6ot", 7)
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
	
	dataLockPoints.acquire()
	current_points = points
	dataLockPoints.release()
	
	suma = 0
	
	print 'zbieranie danych ..'
	
	for i in range(0,10):		
		dataLockPoints.acquire()
		current_points = points
		suma = suma + len(points)
		dataLockPoints.release()
		rospy.sleep(0.5)
		
	print 'dane zebrane!'
		
	avg = suma / 10
	
	dataLockPoints.acquire()
	current_points = points
	dataLockPoints.release()
	
	dataLockPnp.acquire()
	current_matrix = matrix
	dataLockPnp.release()
	
	print 'czekamy na dobre kontury :)'
	
	while len(current_points) > avg:
		dataLockPnp.acquire()
		current_matrix = matrix
		dataLockPnp.release()
		
		dataLockPoints.acquire()
		current_points = points
		dataLockPoints.release()
		
		print suma, len(current_points)
		
	variable = raw_input('podloz czysta kartke: nacisnij cokolwiek!')
	print 'ok!'
	
	dataLockPnp.acquire()
	current_matrix = matrix
	dataLockPnp.release()
	
		
		
	
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
	nextContour = False
	z = irpos.get_cartesian_pose().position.z
	nop = 0
	
	transformation = TBG * camera_to_tl6  * optical_to_camera * current_matrix
	
	
	
	#~ while not rospy.is_shutdown():
		#~ rospy.sleep(1.0)
		
	# NARYSUJ OBRYS KARTKI - pierwszy kontur
	p0 = numpy.matrix([[0.0],[0.0],[0.0],[1]])	
	p1 = numpy.matrix([[0.21],[0.0],[0.0],[1]])
	p2 = numpy.matrix([[0.21],[0.297],[0.0],[1]])
	p3 = numpy.matrix([[0.0],[0.297],[0.0],[1]])
	
	goodPoints = []
	
	obrys = [0.0, 0.0, 0.21, 0.0, 0.21, 0.297, 0.0, 0.297]

	#current_points.append(obrys)
	
	
	if current_points:
			
		for contour in current_points:
			goodContour = []
			for i in range(0,len(contour)-1,2):					
                		
				#punkt w ukladzie kartki
				point = numpy.matrix([[contour[i]],[contour[i+1]],[0],[1]])			
				 #punkt w ukladzie robota	
				point = transformation * point			
						
				point[2] = point[2] + 0.37				
									
				if not checkPoint(point):
					print "point error!"
				else:
					if checkPoint(point):
						goodContour.append(point)
					else:
						print "punkt poza zakresem"
					
			if len(goodContour) > 1:
				goodPoints.append(goodContour)
		
		nextContour = False
		first = True
		
		orientacja = irpos.get_cartesian_pose().orientation
		
		
		

			
		
		 
		
		
		
				
		for contour in goodPoints:
			point = contour[0]
			pointsVector = []
			czas = 0.5
			odleglosc = 0.0
			
			if first:
				variable = raw_input('zacznij rysowac: nacisnij cokolwiek!')
				print 'ok'
				first = False
			
			if nextContour:
				print "podnosi"
				irpos.move_rel_to_cartesian_pose(1.5, Pose(Point(0.0, 0.0, -0.03), Quaternion(0.0, 0.0, 0.0, 1.0)))	
				print "podniesione"
			else:
				nextContour = True
					
			print "pierwszy punkt w konturze - jedzie"		
			irpos.move_to_cartesian_pose(3.0, Pose(Point(point[0], point[1], point[2]), orientacja))
			print "pierwszy punkt w konturze - dojechal"
			
			print "zjedz do kartki"
			irpos.move_rel_to_cartesian_pose_with_contact(5.0, Pose(Point(0.0, 0.0, 0.1), Quaternion(0.0, 0.0, 0.0, 1.0)), Wrench(Vector3(0.0,0.0,5.0),Vector3(0.0,0.0,0.0)))
			irpos.move_rel_to_cartesian_pose(0.3, Pose(Point(0.0, 0.0, -0.003), Quaternion(0.0, 0.0, 0.0, 1.0)))	
			print "zjechal"
			z = irpos.get_cartesian_pose().position.z
			oldPoint = point
			
			irpos.conmanSwitch([irpos.robot_name+'mForceTransformation'], [], True)
			
			for p in contour[1:]:
				diff = math.sqrt(abs(pow(p[0] - oldPoint[0], 2) + pow(p[1] - oldPoint[1], 2)))
				czas = czas + diff / 0.03
				odleglosc = odleglosc + diff
				pointCartTraj = CartesianTrajectoryPoint(rospy.Duration(czas), Pose(Point(p[0], p[1], z), orientacja), Twist())	
				pointsVector.append(pointCartTraj)
				oldPoint = p
				
			print "jedz wzdluz trajektorii"
			irpos.move_along_cartesian_trajectory(pointsVector)
			print "pojechal wzdluz trajektorii"
			#~ print pointsVector
			#~ print "***********"	
			print "odl: ", odleglosc
			print "czas: ", czas
			
			irpos.conmanSwitch([], [irpos.robot_name+'mForceTransformation'], True)
			
			
			
		
		move.podnies(5.0)
		move.pozycjaRobocza(10.0)
		irpos.move_rel_to_cartesian_pose(7.0, Pose(Point(0.1, 0.0, -0.15), Quaternion(0.0, 0.0, 0.0, 1.0)))	
				
					

		
		
		
		



















		
	
	
