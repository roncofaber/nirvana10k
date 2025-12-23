#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 15:24:53 2025

@author: roncofaber
"""

# internal modules
from nirvana10k.measurements.uvvis import NirvanaUVVis

# echfive
import h5py

#%%

def get_sample_data(h5group, poskey):
    
    sample_name   = h5group[poskey]['sample_name'][()].decode('utf-8')
    
    absorbances = h5group[poskey]['absorbance_data'][()]
    intensities = h5group[poskey]['intensity_data'][()]
    spectras    = h5group[poskey]['intensity_data'][()]
    
    x_center = h5group[poskey]['x_center'][()]
    y_center = h5group[poskey]['y_center'][()]
    
    y_positions = h5group[poskey]['y_positions'][()]
    #x_positions = h5group[poskey]['x_positions'][()] #TODO add x_positions
    # for now returns None
    
    return sample_name, absorbances, intensities, spectras, x_center,\
        y_center, y_positions, None

def h5_to_samples(h5filename, erange=None):
    
    samples_list = []
    
    with h5py.File(h5filename, 'r') as h5file:
        
        # get wavelengths (same for all measurments)
        wavelengths = h5file['measurement/pollux_oospec_multipos_line_scan/wavelengths'][()]
        
        # isolate relevant H5 group and get list of positions
        h5group   = h5file['measurement/pollux_oospec_multipos_line_scan/positions']
        positions = h5group.keys()
        
        # read each position and return Nirvana10kSample class
        for poskey in positions:
            
            # read here
            sample_name, absorbances, intensities, spectras, x_center,\
                y_center, y_positions, x_positions = get_sample_data(h5group, poskey)
                
            # make it an object
            uvvis_sample = NirvanaUVVis(sample_name, poskey, wavelengths,
                                        absorbances, intensities, spectras,
                                        x_center, y_center, x_positions, y_positions,
                                        dark_sample=None, blank_sample=None, erange=erange)
            
            # TODO we assume dark and blank always come first --> would fail otherwise!
            if "dark_ref" in sample_name:
                dark_sample  = uvvis_sample
            elif "blank_ref" in sample_name:
                blank_sample = uvvis_sample
            
            else:
                # here we create a new sample -- assume that dark and blank always come first
                uvvis_sample.set_references(dark_sample=dark_sample, blank_sample=blank_sample)
                
                
                samples_list.append(uvvis_sample)
                
    return samples_list