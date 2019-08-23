import os
import sys
import subprocess
import commands

file_with_bad_tr = '/Users/nanditharajamani/Desktop/IIT_delhi_stuff/Assignment_IIT_delhi/fsl_preprocessed/preproc/fsl_preprocess/smooth_img/sub-MSC01_ses-func01_task-motor_run-01_bold_brain_mcf_st_smooth.nii.gz'
#output only the pixel dmensions, the pixdim4 is the TR.
get_header = commands.getstatusoutput('fslinfo {0} | grep "pixdim"'.format(file_with_bad_tr))
#this will split the str with all the pixdim values
split_str = str.split(get_header[1])
#we can change the pixdim values with fsl's fslchpixdim
#$fslchpixdim <xdim> <ydim> <zdim> <tdim> ##DO NOT CHANGE THE xdim,ydim,zdim!!!!
pixdim1 = split_str[1]
pixdim2 = split_str[2]
pixdim3 = split_str[3]
pixdim4 = 2.2 #This is the correct TR
os.system('fslchpixdim %s %s %s %s %s'%(file_with_bad_tr,pixdim1,pixdim2,pixdim3,pixdim4))
