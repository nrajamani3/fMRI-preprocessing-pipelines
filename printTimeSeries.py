#!/usr/bin/python2.7

import nipype as np 
import nibabel as nb
import numpy as np
import sys


ip_file_path = sys.argv[1] #provide path to image file
x_cord = int(sys.argv[2]) #provide x coordinate
y_cord = int(sys.argv[3]) #provide y coordinate of voxel
z_cord = int(sys.argv[4]) #provide z coordinate of voxel


load_ip_img = nb.load(ip_file_path) #load nifti image 
ip_img = load_ip_img.get_data()
ip_img = np.array(ip_img) #convert to an array object
ip_img_shape = ip_img.shape
print(ip_img_shape) #for your reference
no_of_slices = ip_img.shape[3]
time_series = [] #list of time series corresponding to a particular x,y,z cord
#ip_img_affine = load_ip_img.get_affine()
#to get the real dimensions, in mm so we can calculate time point
#ip_mm = nb.affines.apply_affine(ip_img_affine,[x_cord,y_cord,z_cord])
time_series.append(ip_img[x_cord,y_cord,z_cord,:]) #this gives an array of len t(t=no of time points)
print(len(time_series))
with open('{0}.txt'.format(sys.argv[5]),'w') as f:
	for item in time_series:
		f.write("%s\n" % item)




