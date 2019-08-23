#!/usr/bin/python

#This script will generate a design.fsf file for the subject. We then proceed to run the design.fsf file using the command
# $ feat design.fsf ---> *Since this is for one subject and an assignment question, we are assuming the basic
#method of launching the feat analysis holds true. If it needs to be generalized, then we have to launch the design file in a customized manner.

import os
import glob
import re

#initialize the overarching directory
#using a hard coded path for now, but should be removed in favor of a parameter to be passed

big_dir = '/Users/nanditharajamani/Desktop/IIT_Delhi_stuff/assignment_data'
#initialize our fsf directory, within the sub dir itself.
fsf_dir = '{0}/fsf'.format(big_dir)
#since we have only one subject, our sub dir is going to have only one path returned.
#I;m not using the usual glob.glob to get all the paths. If you use glob.glob and more subjects, then
#then you can append it sequentially to sub dir list
sub_dir = "{0}/sub_001/func/sub-MSC01_ses-func01_task_motor_run-01_bold.nii.gz".format(big_dir)
sub_dir_list = []
sub_dir_list.append(sub_dir)


#now we make all the sub_dir a list so we can loop through all subjects, again in this case, just 1.
for dir in sub_dir_list:
#since we have only one subject, I'm going to comment out the run numbers and subject numbers etc
    split_dir = dir.split('/')
    search_sub = re.compile("sub_[0-9][0-9][0-9]")
    current_sub = str((filter(search_sub.match,split_dir)))
    print("Current subject {0} is running".format(current_sub))
#get the run number
    search_run = re.compile(".*run*")
    current_run = str((filter(search_run.match,split_dir)))
    print("Current run is {0}".format(current_run))
#get the number of time points, using fslnvols:
    n_times = os.popen('fslnvols {0}'.format(dir)).read()
#There are a few things we have to change in the design.fsf template file, as it loops through each subject
    to_replace = {{'SUBNUM':current_sub,'NTPTS':n_times,'RUNNUM':current_run}}
#replace the stuff in design_template.fsf
    with open("{0}/design_template.fsf".format(fsf_dir)) as infile:
       with open("{0}/design_{1}_{2}.fsf".format(fsf_dir,current_sub,current_run),'w') as outfile:
           for line in infile:
               for src,target in rreplacements.iteritems():
                   line = line.replace(src,target)
                outfile.write(line)





