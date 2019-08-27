#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import glob
import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe
from nipype.interfaces.fsl import ImageStats


# rom nose.tools import *
## This script runs the warp_nipype workflow to execute the interfaces and with the inputs already provided
## It accepts as it's arguments the input which you'd give the warp_nipe file, an output_dir which can be either be mentioned or if it is set to none will write it in the current working directory.
## The argument run can either be tset to true(default) or to false. If set to false, it should connect to the nipype workflow and return the workflow object instead
##What all should it return?: if the run had been set to true, it would generate the filepath of the output from the workflow. If the run was set to false, then it will return the file path of the
##base directory, the workflow object, etc.
def run_warp_nipype(inputs, output_dir=None, run=True):
    import preprocessing_strat
    warp_workflow = pe.Workflow(name='preproc')
    if output_dir == None:
        output_dir = '/Users/nanditharajamani'

    workflow_dir = os.path.join(output_dir, "preprocessed_output")
    warp_workflow.base_dir = workflow_dir
    # taken from QAP files
    # resource_pool = {}

    num_of_cores = 1
    # resource_pool({'epireg': (warp_nipype2.warp_nipype, 'outputspec.epireg')})
    t_node = EPI_DistCorr.create_EPI_DistCorr()  ####
    t_node.inputs.inputspec.anat_file = '/Users/nanditharajamani/'
    t_node.inputs.inputspec.dcm_dir = '/Users/nanditharajamani/dicomm/nki_5/dicom/triotim/mmilham/discoverysci_30001/A00055806/433946461_V2/BREATH_HOLD_1400_0008'
    t_node.inputs.inputspec.slice_timings_file = '/Users/nanditharajamani'
    t_node.inputs.inputspec.TR = 2.46
    # 'home/nrajamani/FieldMap_SubjectExampleData/SubjectData/epi_run2/fMT0160-0015-00003-000003-01_BRAIN.nii.gz',
    #   for image in inputs:
    #       if not(image.endswith('.nii') or image.endswith('.nii.gz')):
    #           raise 'The input image is not the right format'
    #   try:
    #       for image in inputs:
    #           size = image.get_shape()
    #           assert len(size) == 3
    #   except:
    #       if len(size) < 3:
    #           raise 'input image is not 3D'
    #   intensity = ImageStats(in_file = t_node.inputs.inputspec.fmap_pha, op_string = '-p 90')
    #   if intensity < 3686:
    #      raise 'input phase image does not have the correct range values'
    dataSink = pe.Node(nio.DataSink(), name='dataSink_file')
    dataSink.inputs.base_directory = workflow_dir
    # node, out_file = resource_pool["epireg"]
    # warp_workflow.connect(t_node,'outputspec.roi_file',dataSink,'roi_file')
    warp_workflow.connect(t_node, 'outputspec.nifti_file', dataSink, 'nifti_file')
    warp_workflow.connect(t_node, 'outputspec.anat_skullstripped', dataSink, 'anat_skullstripped')
    warp_workflow.connect(t_node, 'outputspec.slice_time_corrected_file', dataSink, 'slice_time_corrected_file')
    warp_workflow.connect(t_node, 'outputspec.temporal_filtering_file', dataSink, 'temporal_filtering_file')
    warp_workflow.connect(t_node, 'outputspec.motion_correction_file', dataSink, 'motion_correction_file')
    warp_workflow.connect(t_node, 'outputspec.registered_file', dataSink, 'registered_file')
    warp_workflow.connect(t_node, 'outputspec.mat_file_reg', dataSink, 'mat_file_reg')
    warp_workflow.connect(t_node, 'outputspec.log_file_reg', dataSink, 'log_file_reg')
    warp_workflow.connect(t_node, 'outputspec.out_trans_matrix', dataSink, 'out_trans_matrix')
    warp_workflow.connect(t_node, 'outputspec.mean_func', dataSink, 'mean_func')
    if run == True:
        warp_workflow.run(plugin='MultiProc', plugin_args={'n_procs': num_of_cores})

    else:
        return warp_workflow, warp_workflow.base_dir


run_warp_nipype(['anat_file', 'dcm_dir', 'slice_timing_file','TR'], output_dir=None, run=True)
