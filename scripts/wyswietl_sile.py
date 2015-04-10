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





def callback(data):
	
	dataLock.acquire()
	print data.wrench.force.z
	dataLock.release()

if __name__ == '__main__':

	
	rospy.Subscriber("irp6ot_arm/wrist_wrench", WrenchStamped, callback)
	irpos = IRPOS("wyswietl_sile", "Irp6ot", 7, "irp6ot_manager")
	
	while not rospy.is_shutdown():
		print "ok"
		rospy.sleep(1.0)
	
	
