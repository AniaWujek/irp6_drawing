#!/usr/bin/env python


from move_irp6 import *
from punkt import *

def createPose(x, y, z, ox, oy, oz, ow):
	position = Point(x, y, z)
	quaternion = Quaternion(ox, oy, oz, ow)

	P = Pose(position, quaternion)
	return P
	

  	

if __name__ == '__main__':
	

	move = move_irp6('test')
	
	#move.pozycjaRobocza(10.0)
	#move.zlapKlocek(5.0)
	#move.zjedzDoKartki(15.0)
	#move.jedzPoKartceStart(5.0, 0.0, 0.01)
	#move.jedzPoKartce(5.0, 0.01, 0.0)
	#move.jedzPoKartce(5.0, 0.0, -0.01)
	#move.jedzPoKartce(5.0, -0.01, 0.0)
	
	#move.jedzPoKartceStop()
	
	
	#p = [punkt(2.0,-1.0), punkt(1.0, -2.0), punkt(-1.0, -2.0), punkt(-2.0, -1.0), punkt(-2.0,1.0), punkt(-1.0,2.0), punkt(1.0,2.0), punkt(2.0, 1.0)]
	p = [punkt(0.0, 0.0), punkt(1.0, 0.0), punkt(1.0, 1.0), punkt(0.0, 1.0), punkt(2.0,-1.0)]
	#move.test(p)
	move.move_cart(p)
	#move.podnies(5.0)
	
  	
  	
	
	
	
	

	print "OK"
