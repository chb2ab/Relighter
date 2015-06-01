import numpy
import sys
from scipy.spatial import distance
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

# List of methods
# euclidKNN(root, prog, images, k)
# eucMat(images)
# floyds(root, prog, neighborhoods)
# MDS(dmatrix, tgtdims)

# Takes in a Tkinter root and label for displaying the progress, an N length list of image vectors (numpy.array) and a k value (int) that decides how many neighbors to find for each image. Finds the k nearest neighbors for each image and returns an NxN 2 dimensional distance matrix (list of lists) where neighbor relations are given by the euclidean distance between points. If 2 points are neighbors there distance equals their euclidean distance, if 2 points are not neighbors there distance is infinite.
def euclidKNN(root, prog, images, k):
	N = len(images)
	neighbormat = [[float("inf") for _ in range(N)] for _ in range(N)]
	neighborlist = []		
	prog['text'] = "Getting Distance Matrix"
	root.update()
	euclideans = eucMat(images)
	for ii in range(N):
		# neighbormat is initialized to infinity and neighbor relations will have finite euclidean distance. All points are neighbors to themselves with a distance of 0.
		neighbormat[ii][ii] = 0
		edges = []
		for jj in range(N):
			if (ii == jj):
				continue
			edgeLen = euclideans[ii][jj]
			edges.append((jj, edgeLen))
		# sort the edgelengths and take the k smallest.
		edges.sort(key=itemgetter(1))
		neighb = 0;
		neighblist = [];
		while neighb < k and neighb < len(edges):
			jj = edges[neighb][0]
			dist = edges[neighb][1]
			neighbormat[ii][jj] = dist
			neighbormat[jj][ii] = dist
			neighblist.append(jj)
			neighb += 1
		neighborlist.append(neighblist)
	return neighbormat, neighborlist
# Takes in an N length list of image vectors (numpy.arrays) and outputs an NxN two dimensional distance matrix containing the euclidean distance between all pairs of points (each point representing an image vector).
def eucMat(images):
	euclideans = distance.pdist(images, 'euclidean')
	euclideans = distance.squareform(euclideans)
	return euclideans
	## SLOW CODE FOR GENERATING DISTANCE MATRIX ##
	#N = len(images)
	#euclideans = [[0 for _ in range(N)] for _ in range(N)]
	#for ii in range(N):
	#	print "\r" + "distance matrix " + str(ii+1) + "/" + str(N),
	#	sys.stdout.flush()
	#	for jj in range(N):
	#		if ii >= jj:
	#			continue
	#		dist = numpy.sqrt( numpy.sum( numpy.power((images[ii] - images[jj]),2)) )
	#		euclideans[ii][jj] = dist
	#		euclideans[jj][ii] = dist
# Takes in a Tkinter root and label for displaying the progress, a 2 dimensional distance matrix (list of lists) and uses floyds algorithm to compute the shortest geodesic distance between all pairs of points. It returns a 2 dimensional distance matrix with the entries corresponding to geodesic distance. 
def floyds(root, prog, neighborhoods):
	N = len(neighborhoods)
	for k in range(N):
		prog['text'] = "geodesics: " + str(k+1) + "/" + str(N)
		root.update()
		for ii in range(N):
			for jj in range(N):
				neighborhoods[ii][jj] = min(neighborhoods[ii][jj], neighborhoods[ii][k] + neighborhoods[k][jj])
	return neighborhoods 
# Takes in an NxN distance matrix (list of lists) and an int tgtdims corresponding to the number of dimensions to embed into. If N >= tgtdims then it returns the embeddings for each point in an Nxtgtdims two dimensional array (numpy.array of numpy.arrays) where the ordering remains unchanged, meaning the first entry of the distance matrix is the first row of the embedded matrix. If N < tgtdims then it returns false.
def MDS(dmatrix, tgtdims):
	N = len(dmatrix)
	if (tgtdims > N):
		return False
	dmatrix = numpy.array(dmatrix)
	# Analysis of Multivariate and High-Dimensional Data, Inge Koch, Theorem 8.3
	dmatrix = dmatrix ** 2
	dmatrix = -0.5 * (dmatrix - (1.0/N) * (numpy.sum(dmatrix, axis=0, keepdims=True) + numpy.sum(dmatrix, axis=1, keepdims=True)) + numpy.sum(dmatrix, keepdims=True)/float(N**2))
	vals, vecs = numpy.linalg.eig(dmatrix)
	idx = vals.argsort()[::-1]
	vals = vals[idx]
	vecs = vecs[:,idx]
	coords = vecs[:,:tgtdims] * numpy.sqrt(vals[:tgtdims])
	return coords





