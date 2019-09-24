#!/usr/bin/python


import fnmatch
import os
import glob
import nibabel as nib
import numpy as np
"""
This script will generate each subjects design.fsf, but does not run it.
It depends on your system how will launch feat - usually a batch feat file will be useful in this regard. 
All credits go to Janette Mumford, whose original script is taken from:

Inputs:
1. Root dir: Set this to the directory where all of the raw fMRI images live
2. Study dir: Set this to the directory where all of the preprocessed images live.

The script assumes there is a template fsf file called: template_lev1.fsf in the fsfdir: which is the root_dir/fsf
The script also assumes that the directory structure is that nki-rs data. For other BIDS complaint data, simple edits are sufficient,
and would make the code easier. (hint: use glob.glob to match your file with a file pattern)

Example:
python generate_sub_fsf.py '/path/to/root/dir' '/path/to/study/dir' 
"""
root_dir = sys.argv[1] # Set this to the directory all of the raw files directories live in
study_dir = sys.argv[2] #where do all the preprocessed directories live?

study_list_of_interest = os.listdir(study_dir)
root_dir_list_of_interest = os.listdir(root_dir)
##uncomment this piece of code if you want to exclude bad subjects, or otherwise want to remove certain folders

#unwanted = ['nki_00','nki_01','nki_17','nki_65','nki_101','nki_104', 'nki_202']
#unwanted_anat = []
#for file in study_list_of_interest:
#    if 'sub_nki_18_' in file:
#        unwanted_anat.append(file)
#    if 'sub_nki_65' in file:
#        unwanted_anat.append(file)
#    if 'sub_nki_101' in file:
#        unwanted_anat.append(file)
#study_list_of_interest = [e for e in study_list_of_interest if e not in unwanted_anat]
#root_dir_list_of_interest = [e for e in root_dir_list_of_interest if e not in unwanted]



# Set this to the directory where you'll dump all the fsf files
# May want to make it a separate directory, because you can delete them all o
#   once Feat runs
fsfdir="%s/fsf"%(root_dir)

func_file_paths = []
anat_file_paths = []
slice_timing_paths = []

for files in root_dir_list_of_interest:
    if 'nki_' in files:
       file_of_interest = os.path.join(root_dir,files,'dicom/triotim/mmilham') 
       for dirpath,dirnames,filenames in os.walk(file_of_interest):
           if 'CHECKERBOARD_' in dirpath:
               for files in filenames:
                   if files.endswith('.nii.gz') and '_' in files and len(files) > 24:
                       func_file_paths.append(os.path.join(dirpath,files))                       
for files in study_list_of_interest:
    if 'sub_nki_' in files:
        for dirpath,dirnames,filenames in os.walk(os.path.join(study_dir,files)):
            if 'CHECKERBOARD_' in dirpath and 'anat_skullstripped' in dirpath:
                for files in filenames:
                    if files.endswith('.nii.gz') and '_brain' in files:
                        anat_file_paths.append(os.path.join(dirpath,files))
for i in range(len(func_file_paths)):
    if i < len(anat_file_paths):                           
        ntime = os.popen('fslnvols {0}'.format(func_file_paths[i])).read().rstrip()                    
        if '1400' in func_file_paths[i]:
            rep_time = 1.4
        elif '645' in func_file_paths[i]:
            rep_time = 0.645
        img = nib.load(func_file_paths[i])
        img_data = img.get_data()
        img_data_np = np.array(img_data)
        t_vox = img_data_np.shape[0]*img_data_np.shape[1]*img_data_np.shape[2]*img_data_np.shape[3]
        op_dir_string = func_file_paths[i].split('/')
        output_dir = '{0}/{1}_{2}_{3}_{4}_{5}'.format(fsfdir,op_dir_string[8],op_dir_string[12],op_dir_string[13],op_dir_string[14],op_dir_string[15])
        print(output_dir)
        replacements = {'output_dir':output_dir, 'ntime':ntime, 'rep_time':rep_time,'func_file':func_file_paths[i],'anat_file': anat_file_paths[i],'t_vox':t_vox}
        with open("%s/template_lev1.fsf"%(fsfdir)) as infile: 
            with open("%s/lev1/design_subrun_%s_%s_%s_%s_%s.fsf"%(fsfdir,op_dir_string[8],op_dir_string[12],op_dir_string[13],op_dir_string[14],op_dir_string[15]), 'w') as outfile:
                for line in infile:
                    for src, target in replacements.iteritems():
                        line = line.replace(src, str(target))
                    outfile.write(line)
