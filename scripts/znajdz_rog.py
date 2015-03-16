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

def callback(data):
    dataLock.acquire()
    global lastData
    lastData = data.data
    dataLock.release()
    
def pozycjaRobocza():
	move.pozycjaRobocza(10.0)
	irpos.move_rel_to_cartesian_pose(15.0, Pose(Point(0.1, 0.0, -0.15), Quaternion(0.0, 0.0, 0.0, 1.0)))	
	
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
	
	#rospy.init_node('znajdz_rog')
	rospy.Subscriber("pnp", Float32MultiArray, callback)
	irpos = IRPOS("znajdowanie_rogu", "Irp6ot", 7, "irp6ot_manager")
	irpos.set_tool_geometry_params( Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
	move = move_track(irpos)
	
	
	#irpos.move_rel_to_cartesian_pose(7.0, Pose(Point(0.0, 0.0, -0.05), Quaternion(0.0, 0.0, 0.0, 1.0)))	
	
	
	pozycjaRobocza()
	
	#for i in range(1, 4):
	#	calculatePosition()
	#	print lastData
	#	rospy.sleep(3)
	
	
	
	
	
	#print irpos.get_joint_position()
	#print irpos.get_cartesian_pose()
	
	

	print "OK"
	
	
	
	
	
	
	
