import math
from irpos import *
from punkt import *

class move_track:
	irpos = None
	
	def __init__(self, irp):
		self.irpos = irp
		
	def pozycjaRobocza(self, czas):
		#ustaw sie pionowo nad kartka
		if czas < 10.0:
			czas = 10.0
		self.irpos.move_to_joint_position([ 0.3, 0, -0.5 * math.pi, 0, 0, 1.5 * math.pi, -0.5 * math.pi], czas)
	
	def zlapKlocek(self, czas):
		#zlap klocek
		if czas < 5.0:
			czas = 5.0
		self.irpos.tfg_to_joint_position(0.065, czas)
	
	def zjedzDoKartki(self, czas):
		#zjedz do kartki
		if czas < 15.0:
			czas = 15.0
		self.irpos.move_rel_to_cartesian_pose_with_contact(czas, Pose(Point(0.0, 0.0, 0.3), Quaternion(0.0, 0.0, 0.0, 1.0)), Wrench(Vector3(0.0,0.0,5.0),Vector3(0.0,0.0,0.0)))
	  	
	def jedzPoKartceStart(self, czas, xTwist, yTwist):
		if czas > 20.0:
			czas = 20.0
		if xTwist > 0.01:
			xTwist = 0.01
		if yTwist > 0.01:
			yTwist = 0.01
		self.irpos.set_tool_physical_params(10.8, Vector3(0.004, 0.0, 0.156))
		self.irpos.start_force_controller(Inertia(Vector3(0.0, 0.0, 20.0), Vector3(0.0, 0.0, 0.0)), ReciprocalDamping(Vector3(0.0, 0.0, 0.0025), Vector3(0.0, 0.0, 0.0)), Wrench(Vector3(0.0, 0.0, 0.1), Vector3(0.0, 0.0, 0.0)), Twist(Vector3(xTwist, yTwist, 0.0), Vector3(0.0, 0.0, 0.0)))
		time.sleep(czas)
	
	def jedzPoKartce(self, czas, xTwist, yTwist):
		if czas > 20.0:
			czas = 20.0
		if xTwist > 0.01:
			xTwist = 0.01
		if yTwist > 0.01:
			yTwist = 0.01
		self.irpos.set_force_controller_goal(Inertia(Vector3(0.0, 0.0, 20.0), Vector3(0.0, 0.0, 0.0)), ReciprocalDamping(Vector3(0.0, 0.0, 0.0025), Vector3(0.0, 0.0, 0.0)), Wrench(Vector3(0.0, 0.0, 1.0), Vector3(0.0, 0.0, 0.0)), Twist(Vector3(xTwist, yTwist, 0.0), Vector3(0.0, 0.0, 0.0)))	
		time.sleep(czas)
	
	def jedzPoKartceStop(self):
		self.irpos.stop_force_controller()

	def podnies(self, czas):
		if czas < 5.0:
			czas = 5.0
		self.irpos.move_rel_to_cartesian_pose(czas, Pose(Point(0.0, 0.0, -0.05), Quaternion(0.0, 0.0, 0.0, 1.0)))
		
	def opusc(self, czas):
		if czas < 7.0:
			czas = 7.0
		self.irpos.move_rel_to_cartesian_pose(czas, Pose(Point(0.0, 0.0, 0.1), Quaternion(0.0, 0.0, 0.0, 1.0)))
		
	
			
	def ustalPredkosc(self, ppunkt):
		x = ppunkt.x
		y = ppunkt.y
		scale = 0.025
		
		if x == 0:
			xpred = 0.0
			if y > 0:
				ypred = 0.015
			else:
				ypred = -0.015
		elif y == 0:
			ypred = 0.0
			if x > 0:
				xpred = 0.015
			else:
				xpred = -0.015
		elif abs(x) > abs(y):
			if x > 0:
				xpred = scale * 0.75
			else:
				xpred = -scale * 0.75
			if y > 0:
				ypred = abs(y / x * scale) * 0.75
			else:
				ypred = -abs(y / x * scale) * 0.75
		else:
			if y > 0:
				ypred = scale * 0.75
			else:
				ypred = -scale * 0.75
			if x > 0:
				xpred = abs(x / y * scale) * 0.75
			else:
				xpred = -abs(x / y * scale) * 0.75
				
		ret = punkt(xpred, ypred)
		return ret
			
	
	def move_rel(self, pointsArray):
		
		dist = sqrt(pointsArray[0].x**2 + pointsArray[0].y**2)
		czas = dist / 1.5
		p = self.ustalPredkosc(pointsArray[0])
		self.jedzPoKartceStart(czas, p.x, p.y)
		
		points = pointsArray[1:]
		
		for p in points:
			dist = sqrt(p.x**2 + p.y**2)
			czas = dist / 1.5
			pp = self.ustalPredkosc(p)
			self.jedzPoKartce(czas, pp.x, pp.y)
			
		self.jedzPoKartceStop()
		
	def move_cart_test(self, pointsArray):
		for i in range(len(pointsArray)-1, 1, -1):
			pointsArray[i].x = pointsArray[i].x - pointsArray[i-1].x
			pointsArray[i].y = pointsArray[i].y - pointsArray[i-1].y
			
		for p in pointsArray:
			print p.x, p.y
		self.test(pointsArray)
		
	def move_cart(self, pointsArray):
		for i in range(len(pointsArray)-1, 1, -1):
			pointsArray[i].x = pointsArray[i].x - pointsArray[i-1].x
			pointsArray[i].y = pointsArray[i].y - pointsArray[i-1].y
			
		self.move_rel(pointsArray)
			
		
	def test(self, pointsArray):
		dist = sqrt(pointsArray[0].x**2 + pointsArray[0].y**2)
		czas = dist / 1.5
		p = self.ustalPredkosc(pointsArray[0])
		print czas, p.x, p.y
		
		points = pointsArray[1:]
		
		for p in points:
			dist = sqrt(p.x**2 + p.y**2)
			czas = dist / 1.5
			pp = self.ustalPredkosc(p)
			print czas, pp.x, pp.y
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
			
	
