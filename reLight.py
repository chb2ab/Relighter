import time
start_time = time.time()

import pdb

from os import listdir
import sys
import scipy.misc
from isomap import euclidKNN, floyds, MDS
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import csv

# Takes in the filetype of the images in a directory (str), the name of the directory (str), and the size ratio to downsample each image (float). Returns a list of image vectors (numpy.arrays) and a list of filenames for each image (str).
def readDir(filetype, sourcedir, downsample):
	imagevects = []
	imagenames = []
	imagelen = 0
	for fle in listdir(sourcedir):
		if fle.endswith(filetype):
			imagelen += 1
			print "\r" + "loading images: " + str(imagelen),
			sys.stdout.flush()
			image = scipy.misc.imread(sourcedir + "/" + fle, flatten = True)
			image = scipy.misc.imresize(image, downsample)
			image = image.flatten()
			imagevects.append(image)
			imagenames.append(fle)
	return imagevects, imagenames

# Takes in a csv filename e.g. 'sphcordsprims200.csv' where each row is a sample and each column is a dimension. Returns a list of lists where each list is a sample and each element of the list is a dimension.
def readCSV(filename):
	imagevects = []
	imagelen = 0
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			imagelen += 1
			print "\r" + "loading images: " + str(imagelen),
			sys.stdout.flush()
			coord = []
			for cell in row:
				coord.append(float(cell))
			imagevects.append(coord)
	return imagevects

if __name__ == "__main__":
	filetype = input("Filetype for images eg 'jpg': ")
	sourcedir = input("Directory of source images eg 'sphereback': ")
	# Read all the images in a given directory
	imagevects, imagenames = readDir(filetype, sourcedir, 0.25)
	# Get k nearest neighbors of each image
	neighbors = euclidKNN(imagevects, 100)	
	# Generate the geodesic distance between all images based on the generated neighborhoods
	neighbors = floyds(neighbors)
	# embed the geodesic distance matrix into target number of dimensions
	coordinates = MDS(neighbors,3)
	
	fig = plt.figure()
	ax = Axes3D(fig)
	# Plot the 3 dimensional embedding
	for ii in coordinates:
		plt.plot([ii[0]], [ii[1]], "ko", zs=[ii[2]])
		
	plt.show()
	
	print
	print("--- %s seconds ---" % (time.time() - start_time))
	
	
	
	
	
