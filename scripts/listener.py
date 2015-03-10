#!/usr/bin/env python
from irpos import *
from std_msgs.msg import *

def callback(data):
    rospy.loginfo(rospy.get_caller_id()+" I heard %s",data.data)
    
    #print "jestem tu!"
    
def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaenously.
    #print "jestem w listenerze!"
    rospy.init_node('listener', anonymous=False)

    rospy.Subscriber("pnp", Float32MultiArray, callback)
    
    print "jestem po subsciberze"

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    listener()
