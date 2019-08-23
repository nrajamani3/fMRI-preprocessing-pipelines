import numpy as np
from scipy.stats import gamma
import nibabel as nib


#probably redundant and have to find a better way to do this
img = nib.load('/Users/nanditharajamani/Desktop/IIT_delhi_stuff/Assignment_IIT_delhi/fsl_preprocessed/smoothed_img/sub-MSC01_ses-func01_task-motor_run-01_bold_mcf_filt_st_smooth.nii.gz')
img_data = img.get_data()
num_vols = img_data.shape[3]
header = img.header
find_pix = header['pixdim']
TR = find_pix[4]
TR=2.2
t_list = np.arange(1,img_data.shape[3],TR)
#define the hrf model
h = gamma.ppf(t_list,6) + -0.5*gamma.ppf(t_list,10)
h = h/max(h)
#read from the covariates file and determine the duration of each task
dur_of_each_task = 15.4
TRperStim = TR*dur_of_each_task
nREPS = 2 #number of times each stimulus is repeated. This can also be obtained from the
#number of rows in the covariates file, for each stimulus
nTRs = TRperStim*nREPS + len(h)
design_matrix = np.zeros(1,nTRs)
#now, let's make each entry at the time point the stimulus was on as 1. the rest will be zero
#left hand stimulus
left_hand_stim = design_matrix
left_hand_stim(1:TRperStim:)
