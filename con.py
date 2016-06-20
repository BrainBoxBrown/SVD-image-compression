#!/usr/bin/python

# Image Compression from reduced single value decomposition
# Jordan Brown 
# 20th June 2016

# run convert -delay 20 -loop 0 *.jpg svd.gif to make the gif


from multiprocessing import Pool
from PIL import Image
import numpy as np
import scipy.misc

def extract_band(band, img):
	'''
		Extract the RGB bands from an image
		0 == Red
		1 == Green
		2 == Blue
	'''
	imgmat = np.array(list(img.getdata(band=band)), int)
	imgmat.shape = (img.size[1], img.size[0])
	imgmat = np.matrix(imgmat)
	return imgmat

def get_RGB_matricies(img):
	'''
		Get the Red, Green and Blue image
		matricies
	'''
	return [extract_band(x, img) for x in range(3)]

def svd(imgmat):
	print "starting svd"
	ret = np.linalg.svd(imgmat)
	print "ending svd"
	return ret

def svd_image_matricies(imgmats):
	'''
		Decompose the RGB matricies into their SVD's
		Returns an array of tupples [U,E,V]
		for each color band
	'''
	pool = Pool(processes=3) 
	res = pool.map(svd, imgmats)
	pool.close()                         
	pool.join()                           
	return res
	

def reconstruct_matrix(U, sigma, V, level):
	'''
		Multiply the reduced matricies 
		U * E * V
		where we reduce them to level many eigen values
	'''
	return np.matrix(U[:, :level]) * np.diag(sigma[:level]) * np.matrix(V[:level, :])


# open the image
img = Image.open('image.png')
# convert the image into 3 arrays of R, G, B values
imgmats = get_RGB_matricies(img)
# Decompose these into their SVD
Ms = svd_image_matricies(imgmats)

for x in range(1,30):
	# reconstruct the matricies
	reconstimgs = [ reconstruct_matrix(U,sigma,V, x**2) for U, sigma, V in Ms]
	# create a new matrix with the reconstructed values
	rgb = np.zeros((img.size[1], img.size[0], 3), dtype=np.uint8)
	rgb[..., 0] = reconstimgs[0] # Red
	rgb[..., 1] = reconstimgs[1] # Green
	rgb[..., 2] = reconstimgs[2] # Blue

	# run convert -delay 20 -loop 0 *.jpg svd.gif to make the gif
	scipy.misc.imsave('animation/outfile{0}.jpg'.format(x), rgb)






