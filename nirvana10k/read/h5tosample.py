#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 15:24:53 2025

@author: roncofaber
"""

# internal modules
from measurements.uvvis import NirvanaUVVis

# echfive
import h5py

#%%

def get_absorbance_data(h5file, poskey):
    return h5file['measurement/pollux_oospec_multipos_line_scan/positions'][poskey]['absorbance_data'][()]


def h5_to_samples(h5filename, erange=None):
    
    nirvana10k_list = []
    
    with h5py.File(h5filename, 'r') as h5file:
        
        # get wavelengths (same for all measurments)
        wavelengths = h5file['measurement/pollux_oospec_multipos_line_scan/wavelengths'][()]
        
        # extract list of positions
        positions = h5file['measurement/pollux_oospec_multipos_line_scan/positions']
        
        # read each position and return Nirvana10kSample class
        for poskey in list(positions.keys()):
            
            if "DarkReference" in poskey:
                dark_abs = get_absorbance_data(h5file, poskey)
            elif "BlankReference" in poskey:
                blank_abs = get_absorbance_data(h5file, poskey)
            
            else:
                # here we create a new sample -- assume that dark and blank always come first
                
                absorbances = get_absorbance_data(h5file, poskey)
                nirvana10k  = NirvanaUVVis(poskey, wavelengths, absorbances, dark_abs, blank_abs,
                                           erange=erange)
                
                nirvana10k_list.append(nirvana10k)
                
    return nirvana10k_list