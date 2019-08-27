#This code helps to retrieve the exact slice timings encoded in the CSA header of a siemens DICOM image

import nibabel as nib
import nibabel.nicom.dicomwrappers as nnd
import os
import glob
import csv

path_of_interest = '/Users/nanditharajamani/dicomm/nki_10/dicom/triotim'
list_of_timings = []
count = 0
for dirpath,dirnames,filenames in os.walk(path_of_interest):
    for files in filenames:
        if files.endswith('.dcm'):
            file_path = os.path.join(dirpath, files)
            a = nnd.wrapper_from_file(file_path)
            imp = a.csa_header['tags']['MosaicRefAcqTimes']
            list_of_timings.append(imp['items'])
            with open('{0}/slice_timings.txt'.format(dirpath), 'w') as f:
                f.write(str(imp['items']))
            count += 1





