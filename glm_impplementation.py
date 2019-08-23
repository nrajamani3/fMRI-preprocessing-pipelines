import numpy as np
import nibabel as nib
import os
import glob
from scipy import signal
from scipy import stats
from scipy.special import gamma
import matplotlib.pyplot as plt

img = nib.load('/Users/nanditharajamani/Desktop/IIT_delhi_stuff/assignment_data/subdata/func/sub-MSC01_ses-func01_task-motor_run-01_bold.nii.gz')
img_data = img.get_data()
num_vols = img_data.shape[3]
header = img.header
find_pix = header['pixdim']
TR = find_pix[4]

img_data = np.array(img_data)
n_regressors = 5
#Getting parameters required for fitting into the formula Y = xB + n
#Y = BOLD time series
#x = regressors of interest (and if needed, regressors of no interest. Here we are not including that)
# b = model parameters of interest(which we have to determine using OLS method).

for i in range(img_data.shape[0]):
    for j in range(img_data.shape[1]):
        for k in range(img_data.shape[2]):
            Y = img_data[i,j,k,:]
# Using the covariates provided in the data, we can model each regressor as the x1,x2,x3,x4,x5 (here there are five
# regressors) - then, we concatenate them horizontally, to form a X matrix, where each column xi is a regressor of interest.
# We are not going to include a Bo intercept in this formula.
# The B matrix will be unknown, and be a vector of B1,B2,B3,B4,B5 (corresponding to five regressors).
# TO DO: how to stimulate noise????????????????
#To create hrf function
hrf_signal = np.zeros((104,5))
t = np.arange(0,Y.shape[0])
hrf_signal_1 = t ** 8.6 * np.exp(-t / 0.547)
print(hrf_signal_1.shape)
hrf_signal_2 = t ** 8.6 * np.exp(-t / 0.547)
hrf_signal_3 = t ** 8.6 * np.exp(-t / 0.547)
hrf_signal_4 = t ** 8.6 * np.exp(-t / 0.547)
hrf_signal_5 = t ** 8.6 * np.exp(-t / 0.547)
    #stats.gamma.pdf(t,6) + -.5*stats.gamma.pdf(t,10)
hrf_signal[:,0] = hrf_signal_1
hrf_signal[:,1] = hrf_signal_2
hrf_signal[:,2]=  hrf_signal_3
hrf_signal[:,3] = hrf_signal_4
hrf_signal[:,4] = hrf_signal_5


#hrf_signal = hrf_signal/max(hrf_signal)

plt.show()

covariate_paths = '/Users/nanditharajamani/Desktop/IIT_delhi_stuff/assignment_data/subdata/covariates'
covariate_files = []
for f in os.listdir(covariate_paths):
    if f != '.DS_Store':
        covariate_files.append(f)

x_regressors_list = []

for i in range(len(covariate_files)):
#convert contents of each file to a matrix
    matrix = np.loadtxt('{0}/{1}'.format(covariate_paths,covariate_files[i]))
#compress them into a list
    x_regressors_list.append(matrix)

x_regressors_list = [l.tolist() for l in x_regressors_list]
x_before = [item for sublist in x_regressors_list for item in sublist]
x = [item for sublist in x_before for item in sublist]
covariate_reference = np.arange(0,Y.shape[0]*TR,TR)

for i in range(len(covariate_reference)):
    covariate_reference[i]=np.round(covariate_reference[i],2)
covariate_reference = covariate_reference.tolist()
#let's define start, stop and duration of each task
start_left_foot_1 = x[0]
duration_left_foot = x[1]
start_left_foot_2 = x[3]

#left hand
start_left_hand_1 = x[6]
duration_left_hand = x[7]
start_left_hand_2 = x[9]

#right foot
start_right_foot_1 = x[12]
duration_right_foot = x[13]
start_right_foot_2 = x[15]

#right hand
start_right_hand_1 = x[18]
duration_right_hand = x[19]
start_right_hand_2 = x[21]
#tongue
start_tongue_1 = x[24]
duration_tongue = x[25]
start_tongue_2 = x[27]
#for item in sublist]
#contents of this list is such that every element of this list contains the start of the
# task, duration of task and the colums specific the number of times the condition is run
#Create a beta matrix that is a column vector of shape (5,)
#Create a 1-d column vector for each regressor

design_matrix= np.zeros((Y.shape[0],5))

#left foot stimulus
X_1 = np.zeros(Y.shape[0])
X_1.shape = (Y.shape[0],1)
for i in range(X_1.shape[0]):
    #X_1[:x_regressors_list[0][0][0] + ] = 1
    X_1[covariate_reference.index(start_left_foot_1):covariate_reference.index(start_left_foot_1)+covariate_reference.index(duration_left_foot)] = 1
    X_1[covariate_reference.index(start_left_foot_2):covariate_reference.index(start_left_foot_2) + covariate_reference.index(duration_left_foot)] = 1

#left hand stimulus
X_2 = np.zeros(Y.shape[0])
X_2.shape = (Y.shape[0],1)
for i in range(X_2.shape[0]):
    X_2[covariate_reference.index(start_left_hand_1):covariate_reference.index(start_left_hand_1)+covariate_reference.index(duration_left_hand)] = 1
    X_2[covariate_reference.index(start_left_hand_2):covariate_reference.index(start_left_hand_2) + covariate_reference.index(duration_left_hand)] = 1
#right foot
X_3 = np.zeros(Y.shape[0])
X_3.shape = (Y.shape[0],1)
for i in range(X_3.shape[0]):
    X_3[covariate_reference.index(start_right_foot_1):covariate_reference.index(start_right_foot_1)+covariate_reference.index(duration_right_foot)] = 1
    X_3[covariate_reference.index(start_right_foot_2):covariate_reference.index(start_right_foot_2)+covariate_reference.index(duration_right_foot)] = 1

#right hand
X_4 = np.zeros(Y.shape[0])
X_4.shape = (Y.shape[0],1)
for i in range(X_4.shape[0]):
    X_4[covariate_reference.index(start_right_hand_1):covariate_reference.index(start_right_hand_1) + covariate_reference.index(duration_right_hand)] = 1
    X_4[covariate_reference.index(start_right_hand_2):covariate_reference.index(start_right_hand_2) + covariate_reference.index(duration_right_hand)] = 1

#tongue
X_5 = np.zeros(Y.shape[0])
X_5.shape = (Y.shape[0],1)
for i in range(X_5.shape[0]):
    X_4[covariate_reference.index(start_tongue_1):covariate_reference.index(start_tongue_1) + covariate_reference.index(duration_tongue)] = 1
    X_4[covariate_reference.index(start_tongue_2):covariate_reference.index(start_tongue_2) + covariate_reference.index(duration_tongue)] = 1

#we have two vectors Y and temp vector. Temp vector is a vector full of zeros.
##we need to find the points equivalent to start and stop time and then those indices within the
#temp vector need to be replaced to one
design_matrix[:,0] = X_1[:,0]
design_matrix[:,1] = X_2[:,0]
design_matrix[:,2]=  X_3[:,0]
design_matrix[:,3] = X_4[:,0]
design_matrix[:,4] = X_5[:,0]

#hrf_transpose = np.transpose(hrf)
X_matrix=signal.convolve2d(design_matrix,hrf_signal)
X_matrix_correct_shape = np.delete(X_matrix,slice(104,207),0)
X_matrix_correct_shape = np.delete(X_matrix_correct_shape,slice(5,9),1)
#stimulate voxels with various selectives
X_transpose = np.transpose(X_matrix_correct_shape)
X_product = np.matmul(X_transpose,X_matrix_correct_shape) #shape is correct
X_product_inv = np.linalg.inv(X_product)
X_y = np.matmul(X_transpose,Y)
beta_hat = np.matmul(X_product_inv,X_y)
print(beta_hat)


## HYPOTHESIS TESTING AND USING A BETTER DESIGN WITH CONTRASTS
