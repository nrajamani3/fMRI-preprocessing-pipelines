#This code helps to retrieve the exact slice timings encoded in the CSA header of a siemens DICOM image

import nibabel as nib
import nibabel.nicom.dicomwrappers as nnd
import os
import glob
import csv

path_of_interest = '/path/to/dicom/folder'
    #'/Users/nanditharajamani/dicomm/nki_5/dicom/triotim/mmilham/discoverysci_30001/A00056306/439818296_V2/REST_CAP_0005'
list_of_dicom = os.listdir(path_of_interest)
os.chdir(path_of_interest)
#this isn't necessary but it might serve as a good QC

list_of_timings = []
file_path_list = []
count = 0

#for dirpath,dirnames,filenames in os.walk(path_of_interest):
for files in list_of_dicom:
    if files.endswith('.dcm'):
        file_path = os.path.join(path_of_interest,files)
        a = nnd.wrapper_from_file(file_path)
        imp = a.csa_header['tags']['MosaicRefAcqTimes']
        list_of_timings.append(imp['items'])
        count += 1
with open('slice_timings.csv', 'wb') as f:
    wr = csv.writer(f)
    wr.writerows(list_of_timings)
first_row = []
for i in range(count):
    first_row.append('Vol_{0}'.format(i))




