#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 17:53:17 2026

@author: roncofaber
"""

# usual
import numpy as np

# internal modules
from nirvana10k.read.h5tosample import h5_to_samples
from nirvana10k.utils.plotting import plot_inhomogenity

#%%

class NirvanaSamples:
    
    def __init__(self, h5files, erange=None):
        
        # make sure it's a list
        if isinstance(h5files, str):
            h5files = [h5files]
        
        samples = []
        for h5file in h5files:
            temp_samples = h5_to_samples(h5file, erange=erange)
            samples.extend(temp_samples)
        
        self._samples = samples
        
        return
    
    @property
    def samples(self):
        return self._samples
    
    # get inhomogenity of samples
    def get_inhomogenity(self, value="cor_intensities", spots=None):
        
        # iterate over samples and get inhomogenity
        inhomogenity = np.array([sample.get_inhomogenity(spots=spots, value=value) for sample in self])
        
        return inhomogenity
    
    def plot_inhomogenity(self, value="cor_intensities", spots=None):
        
        inhomogenity = self.get_inhomogenity(value=value, spots=spots)
        
        plot_inhomogenity(inhomogenity)
        return
    
    # make class iterable
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, index):
        return self.samples[index]

    def __setitem__(self, index, value):
        self.samples[index] = value
    
    def __delitem__(self, index):
        del self.samples[index]
    
    def __contains__(self, sample):
        return sample in self.samples