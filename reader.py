import csv
from os import listdir
import scipy.misc

# List of methods
# readDir(root, prog, filetype, sourcedir, downsample)
# readCSV(root, prog, filename)

# Takes in the filetype of the images in a directory (str), the name of the directory (str), the size ratio to downsample each image (float), and a . Returns a list of image vectors (numpy.arrays) and a list of filenames for each image (str).
def readDir(root, prog, filetype, sourcedir, downsample):
	images = []
	imagevects = []
	imagenames = []
	imagelen = 0
	for fle in listdir(sourcedir):
		if fle.endswith(filetype):
			imagelen += 1
			prog['text'] = "loading images: " + str(imagelen)
			root.update()
			image = scipy.misc.imread(sourcedir + "/" + fle, flatten = True)
			images.append(image)
			image = scipy.misc.imresize(image, downsample)
			image = image.flatten()
			imagevects.append(image)
			imagenames.append(fle)
	return imagevects, imagenames, images

# Takes in a csv filename e.g. 'sphcordsprims200.csv' where each row is a sample and each column is a dimension. Returns a list of lists where each list is a sample and each element of the list is a dimension.
def readCSV(root, prog, filename):
	imagevects = []
	imagelen = 0
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			imagelen += 1
			prog['text'] = "loading images: " + str(imagelen)
			root.update()
			coord = []
			for cell in row:
				coord.append(float(cell))
			imagevects.append(coord)
	return imagevects, []