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
import tf_conversions.posemath as pm


dataLock = threading.Lock()


licznik = 0;
sily = [0,0,0,0,0]


def callback(data):

	global licznik
	global sily
	dataLock.acquire()	
	#sily[licznik] = data.wrench.force.z
	#licznik = (licznik + 1) % 3
	if data.wrench.force.z > 0:
		sily[licznik] = data.wrench.force.z
		#print data.wrench.force.z
		licznik = (licznik + 1) % 5
	dataLock.release()

if __name__ == '__main__':

	
	rospy.Subscriber("irp6ot_arm/wrist_wrench", WrenchStamped, callback)
	irpos = IRPOS("wyswietl_sile", "Irp6ot", 7, "irp6ot_manager")

	#irpos.conmanSwitch([irpos.robot_name+'mPoseInt', irpos.robot_name+'mForceTransformation'], [], True)
	
	
	
	
	irpos.set_tool_physical_params(10.8, Vector3(0.004, 0.0, 0.156))
	irpos.start_force_controller(Inertia(Vector3(20.0, 20.0, 20.0), Vector3(0.0, 0.0, 0.0)), ReciprocalDamping(Vector3(0.0025, 0.0025, 0.0025), Vector3(0.0, 0.0, 0.0)), Wrench(Vector3(0.0, 0.0, 7.0), Vector3(0.0, 0.0, 0.0)), Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 0.0)))
	irpos.set_force_controller_goal(Inertia(Vector3(20.0, 20.0, 20.0), Vector3(0.0, 0.0, 0.0)), ReciprocalDamping(Vector3(0.0025, 0.0025, 0.0025), Vector3(0.0, 0.0, 0.0)), Wrench(Vector3(0.0, 0.0, 7.0), Vector3(0.0, 0.0, 0.0)), Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 0.0)))	

	#rospy.sleep(1.0)
	
	while sum(sily) / len(sily) < 3.0:
		
		
		
		rospy.sleep(0.01)	
		
	print "BYLA SILA"
	irpos.stop_force_controller()
		
		
		
		

	#irpos.conmanSwitch([], [irpos.robot_name+'mPoseInt', irpos.robot_name+'mForceTransformation'], True)
	
	
