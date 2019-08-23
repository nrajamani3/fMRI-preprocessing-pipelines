#!/usr/bin/python2.7
#This is a program to align all the slices to a target time
#it takes in the value of
# i) Image file path
# ii) TR
# iii) target time
# iv) output file name

import nibabel as nib
import numpy as np
import sys
import matplotlib.pyplot as plt

img_path_file = sys.argv[1]
TR = float(sys.argv[2])  ##TR here can also be obtained from the slice time acquisition txt
slice_aq_file = sys.argv[3]
tar_time = float(sys.argv[4])
outputFileName = sys.argv[5]
img = nib.load(img_path_file)
img_data = img.get_data()


# acquisition parameters
slice_aq_list = []
slice_aq_list = [line.strip() for line in open(slice_aq_file)]
slice_aq_list = [float(x) for x in slice_aq_list]
# example for slice 2
#number of slices
n_z = len(slice_aq_list)
#this will give us the number of slices that are unique (i.e., not repeated)
n_unique = len(set(slice_aq_list))
#Initialize an array of how the target time proceeds (tar_time,TR+tar_time,2TR+tar_time,....)
times = []
for i in np.arange(n_unique):
    times.append(tar_time + i*TR)
#An array to finally append all the generated volumes
slice_timed_odd = []
# okay so now let's get to interpolating. Since we need a slice time corrected output
# file,
# Use interpolation formula. we know the value of a slice at time t, t+TR, t+2TR,.., and we use
# this data to find the value of the slice at target time.
# This will output a matrix y that is also of size y_1 and y_2, which will be the value of slice 2 at time point "t" that we have chosen
# to generalize for each slice, we can now do:
print(len(times))
for i in range(1,len(times)):
    for j in range(1, n_unique +1):
        if i < len(times)-1:
            x = times[i]
            x_1 = slice_aq_list[j - 1] + (i-1)*TR
            x_2 = x_1 + TR
            y_1 = img_data[:, :, (i-1)*n_unique+j-1, :]
            y_2 = img_data[:, :, i*n_unique+j-1, :]
            y = y_1 + (x - x_1) * ((y_2 - y_1) / (x_2 - x_1))
            slice_timed_odd.append(y)
#for the last slice, just use the same values as you would have used for the value
#befor the last
        if i == len(times)-1:
            x = times[i]
            x_1 = slice_aq_list[j-1]+(i-1)*TR
            x_2 = x_1 + TR
            y_1 = img_data[:,:,(i-2)*n_unique+j-1,:]
            y_2 = img_data[:,:,(i-1)*n_unique+j-1,:]
            y = y_1 + (x - x_1) * ((y_2 - y_1) / (x_2 - x_1))
            slice_timed_odd.append(y)

#Replace the image data with the slice time corrected image
img_data= np.stack(slice_timed_odd,axis=2)
print(img_data.shape)
# outputs
#Save as a nifti image
corrected_img = nib.Nifti1Image(img_data, np.eye(4))
nib.save(corrected_img, '{0}.nii.gz'.format(outputFileName))
with open('{0}.txt'.format(outputFileName), 'w') as f:
    # for deciding whether the success or failure of the program

    if (max(slice_aq_list)) == TR:
        f.write("SUCCESS")
        f.close()
    else:
        f.write("FAILURE")
        f.close()
