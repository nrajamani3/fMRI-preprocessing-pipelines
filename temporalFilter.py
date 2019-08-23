#!/usr/bin/python
import nibabel as nib
import numpy as np 
from matplotlib import pyplot as plt 
import sys
from scipy.fftpack import fft,ifft
from scipy.ndimage import gaussian_filter
import math
#This is a program to temporally filter (high pass filtering - i.e., pass high frequencies, but not low ones)
#It takes in an input image path, the TR, the cut off frequency and the output file name to 
#finally produce a version of the input image that is high pass filtered.
input_img_path = sys.argv[1] #path to input image, str
TR = float(sys.argv[2]) #TR value, float
cut_off_time = float(sys.argv[3]) # cut off time, float
output_file_name = sys.argv[4] # output file name, str
#load input image
input_img = nib.load(input_img_path)
input_img_data = input_img.get_data()

#obtain cut off frequency from cut off time
cut_off_fq = 1/cut_off_time
#fourier transform the input image
fourier_input_img = fft(input_img_data)
#set all frequencies below the cut off frequency to be 0
#performing this operation for each voxel corresponding to a time point
temporally_smoothed_img = np.empty((input_img_data.shape[0],input_img_data.shape[1],input_img_data.shape[2],input_img_data.shape[3]))
#set all values below the cut off frequecy to be zero
input_img_data[input_img_data <= cut_off_fq] = 0
#inverse fourier transform to reobtain the actual image
filtered_img = ifft(input_img_data)
#save the filtered image with the given name
filtered_img_save = nib.Nifti1Image(filtered_img,np.eye(4))
nib.save(filtered_img_save,'{0}.nii.gz'.format(output_file_name)) 