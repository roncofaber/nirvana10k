#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 10:42:15 2025

@author: roncofaber
"""

# numpy is my rock and scipy is my gospel
import numpy as np
import scipy
from scipy.integrate import simpson

# plotting stuff
import matplotlib.pyplot as plt
import seaborn as sns
cm = 1/2.54  # centimeters in inches
sns.set_theme(style="white")
sns.set_style("ticks")
fs = 10

#%%

class NirvanaUVVis:
    
    def __init__(self, sample_name, position_key, wavelengths, absorbances,
                 intensities, spectras, x_center, y_center, x_positions, y_positions,
                 dark_sample=None, blank_sample=None, erange=None):
        
        # assign internal variables according to input
        
        # dataset ID
        self.poskey      = position_key
        self.sample_name = sample_name
        
        # measurement data
        self._wavelengths = wavelengths
        self._absorbances = absorbances
        self._intensities = intensities
        self._spectras    = spectras
        
        # set sample position
        self.x_center = x_center
        self.y_center = y_center
        self.x_positions = x_positions
        self.y_positions = y_positions
        
        # reference data
        self.set_references(dark_sample=dark_sample, blank_sample=blank_sample)
        
        # assign energy range (if provided)
        if erange is None:
            self.set_erange((-np.inf, np.inf))
        else:
            self.set_erange(erange=erange)
        
        return
    
    # define bunch of properties so that they are already masked with the correct
    # energy range
    @property
    def wavelengths(self):
        return self._wavelengths[self._emask]
    
    @property
    def absorbances(self):
        return self._absorbances[:,self._emask]
    
    @property
    def intensities(self):
        return self._intensities
    
    @property
    def spectras(self):
        return self._spectras[:,self._emask]
    
    @property
    def nspots(self):
        return len(self.absorbances)

    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
    
    # set erange
    def set_erange(self, erange=None, left=None, right=None):
        if erange is not None:
            self._erange = erange
        if left is not None:
            self._erange[0] = left
        if right is not None:
            self._erange[1] = right
            
        self._setup_emask()
        return
    
    # set references (blank, dark)
    def set_references(self, dark_sample=None, blank_sample=None):
        self._dark_sample  = dark_sample
        self._blank_sample = blank_sample
        return
    
    # set proper mask according to erange
    def _setup_emask(self):
        eleft, eright = self._erange
        self._emask = (self._wavelengths >= eleft) & (self._wavelengths <= eright)
        return
    
    # get inhomogenity within sample
    def get_inhomogenity(self, spots=None):
        
        if self.nspots < 2:
            raise ValueError("At least two spots are required to calculate inhomogeneity.")
        
        if spots is None:
            spots = list(range(self.nspots))
        
        abs_diffs = []
        for cc, ii in enumerate(spots):
            for jj in spots[cc+1:]:
                
                abs_diff  = np.abs(self.absorbances[jj] - self.absorbances[ii])
                area_diff = simpson(abs_diff, self.wavelengths)
                abs_diffs.append(area_diff)
        
        return np.array(abs_diffs)
    
    def plot_sample(self, spots=None):
        
        
        if spots is None:
            spots = list(range(self.nspots))
        
        fig, ax = plt.subplots(figsize=(9.5*cm, 6*cm))
        
        for absorbance in self.absorbances[spots]:
            
            ax.plot(self.wavelengths, absorbance)
        
        ax.set_title(self.poskey)
        
        ax.set_xlabel("Wavelength [nm]", fontsize=fs)
        ax.set_ylabel("Absorbance [-]", fontsize=fs)
        ax.yaxis.set_tick_params(labelsize=fs-1)
        ax.xaxis.set_tick_params(labelsize=fs-1)
        
        ax.set_xlim(left=self._erange[0], right=self._erange[1])
        
        fig.tight_layout()
        fig.show()
        
        return
