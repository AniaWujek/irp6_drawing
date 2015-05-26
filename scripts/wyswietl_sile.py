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
	irpos.conmanSwitch([irpos.robot_name+'mForceTransformation'], [], True)
	
	while not rospy.is_shutdown():
		
		#print "                  ", sum(sily) / len(sily)
		if sum(sily) / len(sily) > 3.0:
			print "JEST"
		else:
			print " "
		
		rospy.sleep(0.01)
		
	irpos.conmanSwitch([], [irpos.robot_name+'mForceTransformation'], True)
	
	
