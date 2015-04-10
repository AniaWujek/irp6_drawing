#!/usr/bin/env python
from irpos import *

if __name__ == '__main__':

    irpos = IRPOS("IRpOS", "Irp6p", 6)
    #pozycja robocza
    irpos.move_to_joint_position([-0.15187268524241074, -1.6179414257668847, -0.15462469491656203, 0.1935714367208079, 4.6702957058994725, -0.18583174994069754], 20.0)
    #opusc i podnies 5cm nad kartka
    irpos.move_rel_to_cartesian_pose_with_contact(20.0, Pose(Point(0.0, 0.0, 0.4), Quaternion(0.0, 0.0, 0.0, 1.0)), Wrench(Vector3(0.0,0.0,2.0),Vector3(0.0,0.0,0.0)))
	irpos.move_rel_to_cartesian_pose(5.0, Pose(Point(0.0, 0.05, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))

	rospy.Subscriber()
