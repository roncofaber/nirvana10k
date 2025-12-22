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
from scipy.signal import savgol_filter

# plotting stuff
import matplotlib.pyplot as plt
import seaborn as sns
cm = 1/2.54  # centimeters in inches
sns.set_theme(style="white")
sns.set_style("ticks")
fs = 10

#%%

class NirvanaUVVis:
    
    def __init__(self, poskey, wavelengths, absorbances, dark_abs, blank_abs,
                 erange=None):
        
        # assign internal variables according to input
        self._poskey      = poskey
        self._wavelengths = wavelengths
        self._absorbances = absorbances
        self._dark_abs    = dark_abs
        self._blank_abs   = blank_abs
        
        if erange is None:
            self.set_erange((-np.inf, np.inf))
        else:
            self.set_erange(erange=erange)
        
        return
    
    @property
    def wavelengths(self):
        return self._wavelengths[self._emask]
    
    @property
    def absorbances(self):
        return self._absorbances[:,self._emask]
    
    def set_erange(self, erange=None, left=None, right=None):
        if erange is not None:
            self._erange = erange
        if left is not None:
            self._erange[0] = left
        if right is not None:
            self._erange[1] = right
            
        self._setup_emask()
        return
            
    def _setup_emask(self):
        eleft, eright = self._erange
        self._emask = (self._wavelengths >= eleft) & (self._wavelengths <= eright)
        return
        
    
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
    
    def plot_sample(self, spots=None, smooth=False):
        
        
        if spots is None:
            spots = list(range(self.nspots))
        
        fig, ax = plt.subplots(figsize=(9.5*cm, 6*cm))
        
        for absorbance in self.absorbances[spots]:
            
            if smooth:
                to_plot = savgol_filter(absorbance, 8, 3)
            else:
                to_plot = absorbance
            
            ax.plot(self.wavelengths, to_plot)
        
        ax.set_title(self._poskey)
        
        ax.set_xlabel("Wavelength [nm]", fontsize=fs)
        ax.set_ylabel("Absorbance [-]", fontsize=fs)
        ax.yaxis.set_tick_params(labelsize=fs-1)
        ax.xaxis.set_tick_params(labelsize=fs-1)
        
        ax.set_xlim(left=self._erange[0], right=self._erange[1])
        
        fig.tight_layout()
        fig.show()
        
        return
    
    @property
    def nspots(self):
        return len(self.absorbances)

