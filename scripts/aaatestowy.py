#!/usr/bin/env python
from irpos import *

from move_track import *
from punkt import *
import math
import threading
from std_msgs.msg import *
from transformations import *

dataLock = threading.Lock()

move = None
lastData = None
sila = None
kontakt1 = False
kontakt2 = False
kontakt3 = False

def callback(data):
    dataLock.acquire()
    global lastData
    lastData = data.data
    dataLock.release()
    
def callbackForce(data):

	global licznik
	global sila
	global kontakt1
	global kontakt2
	global kontakt3
	dataLock.acquire()	
	sila = data.wrench.force.z
	if sila > 5.0:
		if kontakt1:
			if kontakt2:
				kontakt3 = True
			else:
				kontakt2 = True
		else:
			kontakt1 = True
		
	dataLock.release()
    
def pozycjaRobocza(czas):
	move.pozycjaRobocza(czas)
	irpos.move_rel_to_cartesian_pose(7.0, Pose(Point(0.1, 0.0, -0.15), Quaternion(0.0, 0.0, 0.0, 1.0)))	
	
def calculatePosition():
	cartPosition = irpos.get_cartesian_pose()
	
	qX = cartPosition.orientation.x
	qY = cartPosition.orientation.y
	qZ = cartPosition.orientation.z
	qW = cartPosition.orientation.w
	
	pX = cartPosition.position.x
	pY = cartPosition.position.y
	pZ = cartPosition.position.z
	
	quaternion = [qX, qY, qZ, qW]
	TBG = quaternion_matrix(quaternion)
	TBG = TBG + numpy.matrix([[0,0,0,pX],[0,0,0,pY],[0,0,0,pZ],[0,0,0,0]])
	
	#TCK = 
	
	
	#get quaternion and position
	
	#TBG = quaternion_matrix(quaternion)
	#TBG = TBG + position
  	

if __name__ == '__main__':

	global move
	
	if len(sys.argv) > 1 :
		arg = sys.argv[1]
		if sys.argv[1] == 'help' :
			print "synchro"
			print "robocza"
			print "chwytak"
			print "dol"
			print "gora"
			print "position"
			sys.exit()
	
	#rospy.init_node('znajdz_rog')
	rospy.Subscriber("pnp", Float32MultiArray, callback)
	irpos = IRPOS("znajdowanie_rogu", "Irp6ot", 7, "irp6ot_manager")

	#irpos = IRPOS("znajdowanie_rogu", "Irp6ot", 7)
	#irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
	move = move_track(irpos)
	
	
	#irpos.move_rel_to_cartesian_pose(7.0, Pose(Point(0.0, 0.0, -0.05), Quaternion(0.0, 0.0, 0.0, 1.0)))	
	
	#irpos.move_to_synchro_position(15.0)	
	#pozycjaRobocza()
	#irpos.tfg_to_joint_position(0.08, 10.0)
	#move.zlapKlocek(10.0)
	
	#move.zjedzDoKartki(15.0)
	#irpos.move_rel_to_cartesian_pose_with_contact(10.0, Pose(Point(0.0, 0.0, 0.10), Quaternion(0.0, 0.0, 0.0, 1.0)), Wrench(Vector3(0.0,0.0,6.0),Vector3(0.0,0.0,0.0)))
	#irpos.move_rel_to_cartesian_pose(15.0, Pose(Point(0.0, 0.3, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
	#move.podnies(5.0)
	#for i in range(1, 4):
	#	calculatePosition()
	#	print lastData
	#	rospy.sleep(3)
	
	#irpos.move_rel_to_cartesian_pose(5.0, Pose(Point(0.0, 0.0, -0.05), Quaternion(0.0, 0.0, 0.0, 1.0)))
	
	if len(sys.argv) > 1 :
		arg = sys.argv[1]
		if sys.argv[1] == 'synchro' :
			irpos.move_to_synchro_position(20.0)
		if sys.argv[1] == 'robocza' :
			pozycjaRobocza(20.0)
		if sys.argv[1] == 'robocza_szybka' :
			pozycjaRobocza(10.0)
		if sys.argv[1] == 'chwytak' :
			irpos.tfg_to_joint_position(0.08, 10.0)
			move.zlapKlocek(10.0)
		if sys.argv[1] == 'dol' :
			move.zjedzDoKartki(20.0)
		if sys.argv[1] == 'gora' :
			move.podnies(5.0)
		if sys.argv[1] == 'position' :
			irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
			print irpos.get_cartesian_pose()
			
		if sys.argv[1] == 'test' :
			#irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
			move.opusc(7.0)
			irpos.move_to_cartesian_pose(15.0, Pose(Point(0.95655, -0.1303105242, irpos.get_cartesian_pose().position.z), irpos.get_cartesian_pose().orientation))
			#irpos.move_rel_to_cartesian_pose_with_contact(10.0, Pose(Point(0.0, 0.0, 0.10), Quaternion(0.0, 0.0, 0.0, 1.0)), Wrench(Vector3(0.0,0.0,6.0),Vector3(0.0,0.0,0.0)))
			print irpos.get_cartesian_pose()
			
		if sys.argv[1] == 'przod' :
			irpos.move_rel_to_cartesian_pose(10.0, Pose(Point(-0.1, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
		
		if sys.argv[1] == 'doldol' :
			irpos.move_rel_to_cartesian_pose(5.0, Pose(Point(0.0, 0.0, 0.05), Quaternion(0.0, 0.0, 0.0, 1.0)))
			irpos.move_rel_to_cartesian_pose(5.0, Pose(Point(0.0, 0.0, 0.05), Quaternion(0.0, 0.0, 0.0, 1.0)))
		
		if sys.argv[1] == 'along' :
			point0 = CartesianTrajectoryPoint(rospy.Duration(3.0), Pose(Point(0.760011624185, -1.70946502728e-06, 1.50), irpos.get_cartesian_pose().orientation), Twist())
			point1 = CartesianTrajectoryPoint(rospy.Duration(6.0), Pose(Point(0.760011624185, -1.70946502728e-06, 1.45), irpos.get_cartesian_pose().orientation), Twist())
			points = []
			points.append(point0)
			points.append(point1)
			irpos.move_along_cartesian_trajectory(points)
			print points
			
		if sys.argv[1] == 'sila_dol' :
			dataLock.acquire()	
			
			
			
			dataLock.release()	
		


		
			
			
	
	
	
	#print irpos.get_joint_position()
	#print irpos.get_cartesian_pose()
	
	

	#print "OK"
	
	
	
	
	
	
	
