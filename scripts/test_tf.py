from transformations import *
import numpy


a = 10
b = 20
c = 30
d = 9
quat = [a, b, c, d]

#quat = [-2.16193853672e-05, 0.999999997597, -6.54983099988e-05, 7.03729988673e-06]

TBG = quaternion_matrix(quat)
TBG = TBG + numpy.matrix([[0,0,0,a],[0,0,0,b],[0,0,0,c],[0,0,0,0]])


TCK = numpy.matrix('0.09426888078451157 0.9955435991287231 0.002521710703149438 -0.1116592139005661; 0.995060920715332 -0.09430170059204102 0.030999962240457535 -0.09682109206914902; 0.03109961561858654 -0.0004130760789848864 -0.9995161890983582 0.8719534873962402; 0 0 0 1')

matrix = numpy.zeros(shape=(4,4))
matrix = numpy.zeros(shape=(3,3))

array = []
myArray1=[1,2,4,6,7,3,2,4,2,2]
myArray2=[3,4]

myArray3 = myArray1[2:5]

array.append(myArray1)
array.append(myArray2)
array.append(myArray3)

arr = numpy.matrix([[0,-1,0,0.0551],[1,0,0,0],[0,0,1,0.27],[0,0,0,1]])

print arr

arr[2,3] = 100

print arr

