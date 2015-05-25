from svd_FitHypersphere import fit_hypersphere
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import copy as c
from isomap import eucMat
import sys

previous = None
xtop = 0
ytop = 0
ztop = 0

# Takes in 
def sphFitting(sphere):
	methods = ["Hyper", "Taubin", "Pratt"]
	datax,datay,dataz = zip(*sphere)	
	fit = fit_hypersphere(sphere,methods[0])

	sphr = fit[0]
	sphx = fit[1][0]
	sphy = fit[1][1]
	sphz = fit[1][2]
	# center the sphere at the origin
	vectorx = [x - sphx for x in datax]
	vectory = [y - sphy for y in datay]
	vectorz= [z - sphz for z in dataz]

	vectorlist = zip(*[vectorx, vectory, vectorz])
	
	coordonsph = [[(vector[0] * sphr /sqrt(pow(vector[0],2)+pow(vector[1],2)+pow(vector[2],2))),(vector[1] * sphr /sqrt(pow(vector[0],2)+pow(vector[1],2)+pow(vector[2],2))),(vector[2] * sphr /sqrt(pow(vector[0],2)+pow(vector[1],2)+pow(vector[2],2))) ]for vector in vectorlist]
	return coordonsph

def sphBase(sphere):
	euclideans = eucMat(sphere)
	area = 0
	indices = []
	for ii in range(len(euclideans)):
		for jj in range(len(euclideans)):
			for kk in range(len(euclideans)):
				s1 = euclideans[ii][jj]
				s2 = euclideans[ii][kk]
				s3 = euclideans[jj][kk]
				p = (s1+s2+s3)/2
				a = sqrt(p*(p-s1)*(p-s2)*(p-s3))
				if a > area:
					area = a
					indices = [ii,jj,kk]
	return indices

def chooseTop(prog, coordinates):
	x,y,z = zip(*coordinates)
	fig = plt.figure()
	ax1 = fig.add_subplot(111, projection='3d')
	ax1.set_title('Pick the Top Point')
	ax1.scatter(x, y, z, c='b',picker=5)
	fig.canvas.mpl_connect('pick_event', lambda event: onpick(event, ax1, prog, fig))
	fig.show()


def onpick(event, ax1, prog, fig):
	global previous, xtop, ytop, ztop
	if (previous != None):
		previous.remove()
	ind = event.ind[0]
	x,y,z = event.artist._offsets3d
	xtop = x[ind]
	ytop = y[ind]
	ztop = z[ind]
	prog['text'] = "Coordinates: (%s, %s, %s)" % (xtop, ytop, ztop)
	previous = ax1.scatter([xtop], [ytop], zs=[ztop], s = 50, c=['r'],picker=5)
	plt.draw()

def getTop():
	return xtop, ytop, ztop


def RotateCords(Cords, angle, axis):
	Cords = np.array(Cords)
	twod = False
	if (len(Cords[0]) == 2):
		twod = True
		Cords = np.append(Cords, [[0] for _ in range(len(Cords))], axis=1)
		Cords = c.copy(Cords).T
	angle = float(angle) * np.pi / 180
	if axis == 'x':
		RotM = [[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]]
	elif axis == 'y':
		RotM = [[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]]
	elif axis == 'z':
		RotM = [[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]]
	ans = np.dot(RotM, Cords)
	if (twod):
		ans = zip(ans[0],ans[1])
	return np.asarray(ans)
	
def GlobalToSphere(Cords):
	x = Cords[0]
	y = Cords[1]
	z = Cords[2]
	
	radius = np.linalg.norm(np.array([x, y, z]))
	theta = 0
	phi = 0
	
	if z == 0:
		theta = np.pi / 2
	else:
		theta = np.arccos(float(z) / radius)
	if x == 0:
		if y > 0:
			phi = np.pi / 2
		if y < 0:
			phi = np.pi * 3 / 2
	if x > 0 and y >= 0:
		phi = np.arctan(float(y)/x)
	if x < 0 and y >= 0:
		phi = np.pi + np.arctan(float(y) / x)
	if x < 0 and y < 0:
		phi = np.arctan(float(y) / x) + np.pi
	if x > 0 and y < 0:
		phi = np.pi * 2 + np.arctan(float(y)/x)
	
	ans = np.array([radius, theta, phi])
	return ans

def Rectify(Cords, dirVec): # rectify Sphere cords with "dirVec" oriantation to z axis
	dirVec = np.array(dirVec)
	Cords = np.array(Cords)
	ans = c.copy(Cords).T
	SphereDir = GlobalToSphere(dirVec)
	phi = - SphereDir[2] * 180 / np.pi
	theta = - SphereDir[1] * 180 / np.pi
	ans = RotateCords(ans, phi, 'z')
	ans = RotateCords(ans, theta, 'y')
	return ans.T.tolist()

def UnfoldSphere(Cords, figRadius = 0):# unfold a Sphere into a 2D circle
	Cords = np.array(Cords)
	SCords = c.copy(Cords)
	ans = np.empty([SCords.shape[0], 2])
	for i in range(SCords.shape[0]):
		SCords[i] = GlobalToSphere(SCords[i])
		ans[i, 0] = np.cos(SCords[i, 2]) * SCords[i, 1]
		ans[i, 1] = np.sin(SCords[i, 2]) * SCords[i, 1]
#		 if (SCords[i, 2] <= (2 * np.pi) and SCords[i, 2] > (3.0 / 2  * np.pi)) or (SCords[i, 2] <= (1.0 / 2 * np.pi) and SCords[i, 2] > 0):
#			 ans[i, 0] = np.cos(SCords[i, 2]) * SCords[i, 1]
#			 ans[i, 1] = np.sin(SCords[i, 2]) * SCords[i, 1]
#	 a = SCords.T
	return ans.tolist()







