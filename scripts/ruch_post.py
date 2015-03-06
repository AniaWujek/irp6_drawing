#!/usr/bin/env python
from irpos import *

from move_post import *
from punkt import *
import math

def createPose(x, y, z, ox, oy, oz, ow):
	position = Point(x, y, z)
	quaternion = Quaternion(ox, oy, oz, ow)

	P = Pose(position, quaternion)
	return P
	

  	

if __name__ == '__main__':
	irpos = IRPOS("rysowanie", "Irp6p", 6)

	move = move_post(irpos)
	
	irpos.move_rel_to_cartesian_pose(7.0, Pose(Point(-0.1, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
	
	#irpos.move_rel_to_cartesian_pose(8.0, Pose(Point(0.05, -0.05, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
	
	#move.pozycjaRobocza(10.0)
	#irpos.move_to_joint_position([0, 0, -0.5 * math.pi, 0, 0, 1.5 * math.pi, -0.5 * math.pi], 20.0)
	#print irpos.get_cartesian_pose()
	#irpos.move_rel_to_cartesian_pose(5.0, Pose(Point(0.03, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 1.0)))
	#print irpos.get_cartesian_pose()
	
	#move.zlapKlocek(5.0)
	#move.zjedzDoKartki(10.0)
	#move.jedzPoKartceStart(5.0, 0.0, 0.01)
	#move.jedzPoKartce(5.0, 0.01, 0.0)
	#move.jedzPoKartce(5.0, 0.0, -0.01)
	#move.jedzPoKartce(5.0, -0.01, 0.0)
	
	#move.jedzPoKartceStop()
	
	
	#p = [punkt(2.0,-1.0), punkt(1.0, -2.0), punkt(-1.0, -2.0), punkt(-2.0, -1.0), punkt(-2.0,1.0), punkt(-1.0,2.0), punkt(1.0,2.0), punkt(2.0, 1.0)]
	#p = [punkt(3.0, 0.0), punkt(0.0, -3.0), punkt(-3.0, 0), punkt(0.0, 3.0)]
	#p = [punkt(0.0, 0.0), punkt(5.0, 0.0), punkt(5.0, 5.0), punkt(0.0, 5.0), punkt(5.0,0.0)]
	#move.move_rel(p)
	#move.move_rel(p)
	#move.test(p)
	#move.move_cart(p)
	#move.podnies(5.0)
	
  	
  	
	
	
	
	

	print "OK"
