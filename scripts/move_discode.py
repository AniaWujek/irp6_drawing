#!/usr/bin/env python
from IRPOS import *
from std_msgs.msg import String

def callback(data):
    print "jestem tu!"
    
def listener():
    print "jestem w listenerze!"
    rospy.init_node('listener')
    
    rospy.Subscriber("int", String, callback)
    
    rospy.spin()


if __name__ == '__main__':
	print "jestem w main!"
	listener()
	

