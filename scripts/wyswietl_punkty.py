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

matrix = None
lastData = None


def callbackPoints(data):
	global matrix
	dataLock.acquire()
	
	ind = 1
	if data.data :
		contours_number = int(data.data[0])
		matrix = []
		for i in range(1,contours_number):
			arraySize = int(data.data[ind])
		
			start = ind+1
			end = ind + arraySize*2 + 1
			matrix.append(data.data[start:end])
			ind = ind + arraySize*2 + 1
	
	dataLock.release()
	
def callbackPointsXY(data):
	global matrix
	dataLock.acquire()
	
	ind = 1
	if data.data :
		contours_number = int(data.data[0])
		matrix = []
		for i in range(1,contours_number):
			arraySize = int(data.data[ind])
		
			start = ind+1
			end = ind + arraySize*2 + 1
			contour = append(data.data[start:end])
			temp = []
			for j in range(0,len(contour)-2,2):
				temp.append([contour[j],contour[j+1])
			ind = ind + arraySize*2 + 1
	
	dataLock.release()
	


if __name__ == '__main__':

	
	rospy.Subscriber("points", Float32MultiArray, callbackPoints)
	
	irpos = IRPOS("wyswietl_punkty", "Irp6ot", 7, "irp6ot_manager")
	
	while not rospy.is_shutdown():
		rospy.sleep(1.0)
		print matrix[3]
	
	
