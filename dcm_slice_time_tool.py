#This code helps to retrieve the exact slice timings encoded in the CSA header of a siemens DICOM image

import nibabel as nib
import nibabel.nicom.dicomwrappers as nnd
import nipype
import zipfile
import os
from nipype.interfaces.dcm2nii import Dcm2niix
import sys
import numpy as np


""""
##This code will perform the initial steps in extracting zipped data from folders, and then getting the slice times from the CSA headers (we assume it is dicom data from a Siemens Scanner)
##The code will also convert the dicom files to nifti format, using the dcm2niix program.
##The slice times are also converted to units of TR, as required by FSL's slice timing program.
##The code takes in as input:
#1. Extraction bool: Would you like the files to be extracted? If you choose no, it is assumed that the root directory will be the directory in which all the files to process are.

#2. The root directory: Please specify the directory where all your data lies, as the second argument in the command to run this code
#3. The directory into which you would like to extract the files: It can be the same as root directory but it is suggested that there are no conflicting filenames in that directory which will prevent it from unzipping. 
    for this case it is assumed you will give a new, clean directory.
#4.  Memory control bool: Please specify if you will require conservation of space. If this is True, then it will delete all the dicom files **after processing**. It is not recommended, unless you are sure you have a backup of the dicom data.

The code will output:
#1. The converted .nii.gz file
#2. slice_timings.txt
#3. new_slice_timings.txt file : slice timing in units of TR, as required for FSL preprocessing. 

Example run:

python dcm_slice_time_tool.py True '/path/to/root/dir' '/dir/to/be/extracted' True

"""
def nki_pre_preprocess(root_dir,path_of_interest,extraction_bool,memory_control_bool):
     
    ##take as command line argument the directory/list of .dcm files
    #output directory as a command line argument
    #specific to our case only, 
    if extraction_bool:
        with zipfile.ZipFile(path_of_interest, 'r') as zip_ref:
            zip_ref.extractall(dir_to_be_extracted)
        created_files = os.listdir(dir_to_be_extracted)
            #os.rename('/mnt/project1/data/fMRI/raw/nki-rs/nanditha/nki', '/mnt/project1/data/fMRI/raw/nki-rs/nanditha/nki_{0}'.format(path_of_interest[51]+path_of_interest[52]+path_of_interest[53]))
   #     except zipfile.BadZipfile:
   #            pass
    else:
        created_files = os.listdir(root_dir)
    
    
    list_of_timings = []
    count = 0
    paths = []
    for created_file in created_files:
        for dirpath,dirnames,filenames in os.walk(created_file):
        #if not os.path.exists('{0}/slice_timings.txt'.format(dirpath)):
            for files in filenames:
                if files.endswith('.dcm'):
                    paths.append(dirpath)
                    file_path = os.path.join(dirpath, files)
                    a = nnd.wrapper_from_file(file_path)
                    imp = a.csa_header['tags']['MosaicRefAcqTimes']
                    list_of_timings = imp['items']
                    with open('{0}/slice_timings.txt'.format(dirpath), 'w') as f:
                        for elem in list_of_timings:
                            f.write("%s\n" % elem)
                    count += 1
    paths = set(paths)
    paths = (list(paths))
    for i in range(len(paths)):
        source = paths[i]
        dcm_to_nii = nipype.interfaces.dcm2nii.Dcm2niix()
        dcm_to_nii.inputs.source_dir = source
        dcm_to_nii.inputs.bids_format = True
        dcm_to_nii.inputs.output_dir = source
        dcm_to_nii.run()
    if memory_control_bool:
        for dirpath,dirnames,filenames in os.walk(created_file):
            for files in filenames:
                if files.endswith('.dcm'):
                    file_path = os.path.join(dirpath, files)
                    os.remove(file_path)


def fsl_slice_timing(created_file):
    new_slice_timings = []
    for dirpath, dirnames, filenames in os.walk(created_file):
        for files in filenames:
            if files.endswith('.txt'):
                with open('{0}/slice_timings.txt'.format(dirpath),'r') as f:
                    slices = f.readlines()
                    timings = [float(e.strip()) for e in slices]
                    timings = [np.round(e, 2) for e in timings]
                    for elem in timings:
                        elem = (elem/max(timings)) - 0.5
                        new_slice_timings.append(elem)
                    with open('{0}/new_slice_timings.txt'.format(dirpath),'w') as f:
                        for elem in new_slice_timings:
                            f.write("%s\n" % elem)

if __name__== '__main__':
#only required if the extraction has stopped abruptly, and you want to resume ignoring th "bad extraction
    extraction_bool = sys.argv[1]
    root_dir = sys.argv[2] #get this from the command line, uncomment before publishing
    dir_to_be_extracted = sys.argv[3] # Specify the path you want to extract the files to.
    memory_control_bool = sys.argv[4] # if you want to conserve space, turn this to TRUE. It will delete dicom files after processing.
    

    list_of_interest  = os.listdir(root_dir)
    dir_of_interest = os.listdir(dir_to_be_extracted)
    #this piece of code can be uncommented when the extraction stopped abruptly and you want to resume from the last known position
    #unwanted = []
    #for i in range(104):
    #    unwanted.append(list_of_interest[i])
    #list_of_interest = [e for e in list_of_interest if e not in unwanted]
    for files in list_of_interest:
        if files.endswith('.zip'): 
            path_of_interest = os.path.join(root_dir,files)
            print(path_of_interest)
            nki_pre_preprocess(root_dir,path_of_interest,extraction_bool,memory_control_bool)
    if extraction_bool:
        files_to_be_processed = os.listdir(dir_to_be_extracted)
    else:
        files_to_be_processed = os.listdir(root_dir)
    
    for file in files_to_be_processed:
        if 'nki_' in file:
            created_file = os.path.join(path,file)
            fsl_slice_timing(created_file)
   



