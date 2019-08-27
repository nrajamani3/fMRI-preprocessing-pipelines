import nibabel as nib
import nipype as np
import nipype.pipeline.engine as pe
from nipype.interfaces import afni,fsl,dcm2nii
import nipype.interfaces.utility as util



def create_preprocessed_nki(wf_name = 'prepoc_nki'):
    preproc = pe.Workflow(name =wf_name)
    inputNode = pe.Node(util.Identity.interface(fields=['dcm_dir','anat_file','slice_timings_file','ref_file','TR']), name='inputspec')

    outputNode = pe.Node(util.Identity.interface(fields=['nifti_file','anat_skullstripped','slice_time_corrected_file', 'temporal_filtering_file', 'motion_correction_file', 'registered_file','mat_file_reg','log_file_reg','out_trans_matrix','mean_func']), name='outputspec')
    ############ converting the dicom files into nii files################

    dcm_to_nii = pe.Node(interface=dcm2nii.Dcmniix(),name='dcm_to_nii')
    dcm_to_nii.inputs.bids_format = True
    preproc.connect(inputNode,'dcm_dir',dcm_to_nii,'source_dir')
    preproc.connect(dcm_to_nii,'converted_files',outputNode,'nifti_file')

    #Let's start with skull stripping the anat files
    anat_skullstrip = pe.Node(interface=fsl.BET(),name='anat_skullstrip')
    anat_skullstrip.inputs.output_type = 'NIFTI_GZ'
    preproc.connect(inputNode,'anat_file',anat_skullstrip,'in_file')
    preproc.connect(anat_skullstrip,'out_file',outputNode,'anat_skullstripped')

    #Now we can get to preprocessing the func files
    slice_time_corr = pe.Node(interface=afni.SliceTimer(),name='slice_time_corr')
    slice_time_corr.inputs.interleaved = True
    preproc.connect(dcm_to_nii,'converted_files',slice_time_corr,'in_file')
    preproc.connect(inputNode,'slice_timings_file',slice_time_corr,'slice_timing')
    preproc.connect(slice_time_corr,'out_file',outputNode,'slice_time_corrected_file')

    #motion correction
    motion_corr = pe.Node(interface=afni.Volreg(),name='motion_corr')
    preproc.connect(slice_time_corr,'out_file',motion_corr,
                    'in_file')
    preproc.connect(motion_corr,'out_file',outputNode,'motion_corrected_file')

    #temporal filtering
    temp_corr = pe.Node(interface=fsl.maths.TemporalFilter(),name='temp_corr')
    #temp_corr.inputs.lowpass = 0.01
    if TR == 1400:
        temp_corr.inputs.highpass_sigma = 35
    elif TR == 645:
        temp_corr.inputs.highpass_sigma = 78
    else:
        temp_corr.inputs.highpass_sigma = 20
    preproc.connect(motion_corr,'out_file',temp_corr,'in_file')
    preproc.connect(temp_corr,'out_file',outputNode,'temporal_filtering_file')

    #co-registration using FLIRT (FSL's Linear Registration tool)
    flirt_reg = pe.Node(interface=fsl.FLIRT(),name=
                        'flirt_reg')
    flirt_reg.inputs.interp = 'nearestneighbour'
    flirt_reg.inputs.save_log = True

    preproc.connect(inputNode,'ref_file',flirt_reg,'reference')
    preproc.connect(temp_corr,'out_file',flirt_reg,'in_file')
    preproc.connect(flirt_reg,'out_file',outputNode,'linear_registered_file')
    preproc.connect(flirt_reg,'out_matrix_file',outputNode,'mat_file_reg')
    preproc.connect(flirt_reg,'out_log',outputNode,'log_file_reg')

    #invert xfm if non linear registration is required
    inv_flirt = pe.Node(interface=fsl.ConvertXFM(),name='inv_flirt')
    preproc.connect(flirt_reg,'out_matrix_file',inv_flirt,'in_file')
    inv_flirt.inputs.invert_xfm = True
    preproc.connect(inv_flirt,'out_file',outputNode,'output_trans_matrix')

    #construct mean functional
    mean_func = pe.Node(interface=fsl.maths.MeanImage(),name='mean_func')
    mean_func.inputs.dimension = 'T'
    preproc.connect(flirt_reg,'out_file',mean_func,'in_file')
    preproc.connect(mean_func,'out_file',outputNode,'mean_func')



    return preproc





