#!/usr/bin/python

import nibabel as nib
import numpy as np 
from matplotlib import pyplot as plt 
import sys
from scipy import ndimage
from scipy.fftpack import fft,ifft
from mpl_toolkits import mplot3d

input_img_path = sys.argv[1]
input_img = nib.load(input_img_path)
input_img_data = input_img.get_data()
fwhm = float(sys.argv[2])
output_file_name = sys.argv[3]

#For carrying out filtering, let us create a smoothing matrix which is of the same
#size as our input matrix.
#TODO: Which numpy array occupis least space?
#We define the smooth matrix with a three simensional gaussian function given
#by the formula f(x,y,z)=-e^(x^2/2sz^2+y^2/2sy^2+z^2/2sz^2). 
#We can now estimate the relationship between FWHM and s(standard deviation) as
#fwhm=2.35s
#but let us define a function that will give us the sigma when we input fwhm
def fwhm2sigma(fwhm):
    sigma = fwhm /np.sqrt(8*np.log(2)) 
    return sigma   

sigma = fwhm2sigma(fwhm)
#In order to smooth an image of resolution 3*3*3 mm3, with a gaussian kernel of FWHM 6mm,
#the required parameters are:
#sx = 6/(2.35*3),sy= 6/(2.35*3), sz= 6/(2.35*3) but here, since there is no res input, we're going to assume
#theresolution and thus the sigma at all directions to be equal
#reference: https://users.fmrib.ox.ac.uk/~stuart/thesis/chapter_6/section6_2.html
#let us apply the gaussian to a multi dimensional image


###kernel building
#this creates a list of points in the x,y and z directions
x=np.arange(-input_img_data.shape[0]/2,input_img_data.shape[0]/2)
y=np.arange(-input_img_data.shape[1]/2,input_img_data.shape[1]/2)
z=np.arange(-input_img_data.shape[2]/2,input_img_data.shape[2]/2)

#3 1D kernels are built
kernel_x = np.exp(-(x ** 2)/(2 * sigma ** 2))
#normalization constant - TODO why is the theoretical normalization constant not giving a good output???
kernel_x = kernel_x/sum(kernel_x)
#we can now multiply the two matrices for each time point and then return the product of the image and the smoothing matrix., i.e., convolution
kernel_y = np.exp(-(y ** 2)/(2*sigma**2))
kernel_y = kernel_y/sum(kernel_y)

kernel_z = np.exp(-(z ** 2)/(2*sigma**2))
kernel_z = kernel_z/sum(kernel_z)
#write the convolve function: TODO why is fft not working???
def convolve1d(ip_img,kernel):
    img_convolved = np.zeros(2*ip_img.shape[0]-1)
    N=ip_img.shape[0]
    for n in range(2*N-1):
	    for m in range(max(n-N+1,0),min(n+1,N)):
		    img_convolved[n] += ip_img[m]*kernel[n-m]
    start = ip_img.shape[0]/2
    stop = ip_img.shape[0] + ip_img.shape[0]/2
    img_convolved = img_convolved[start:stop]
    return img_convolved        

#empty matrix which will take final matrices place
smoothed_matrix = np.zeros((input_img_data.shape[0],input_img_data.shape[1],input_img_data.shape[2],input_img_data.shape[3]))
#convolving x direction arrays with kernel_x 
for i in range(input_img_data.shape[1]):
    for j in range(input_img_data.shape[2]):
        for k in range(input_img_data.shape[3]):
            smoothed_matrix[:,i,j,k] = convolve1d(input_img_data[:,i,j,k],kernel_x)
#convolving y direction arrays with kernel_y 
for i in range(input_img_data.shape[0]):
    for j in range(input_img_data.shape[2]):
        for k in range(input_img_data.shape[3]):
            smoothed_matrix[i,:,j,k] = convolve1d(smoothed_matrix[i,:,j,k],kernel_y)
#convolving z direction arrays with kernel_z 
for i in range(input_img_data.shape[0]):
    for j in range(input_img_data.shape[1]):
        for k in range(input_img_data.shape[2]):
            smoothed_matrix[i,j,:,k] = convolve1d(smoothed_matrix[i,j,:,k],kernel_z)

#save smoothed image
print(smoothed_matrix.shape)
smoothed_img_save = nib.Nifti1Image(smoothed_matrix,np.eye(4))
nib.save(smoothed_img_save,'{0}.nii.gz'.format(output_file_name))