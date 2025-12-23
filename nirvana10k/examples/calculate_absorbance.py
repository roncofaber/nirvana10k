#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 17:15:46 2025

@author: roncofaber
"""

import h5py
import matplotlib.pyplot as plt

filename = "251210_173817_pollux_oospec_multipos_line_scan.h5"

h5file = h5py.File(filename)

#%%


def get_hdf5_structure(name, obj):
    """Recursively get the structure of an HDF5 file."""
    if isinstance(obj, h5py.Group):
        return (name, True, [get_hdf5_structure(name + '/' + k, obj[k]) for k in obj])
    elif isinstance(obj, h5py.Dataset):
        return (name, False, None)  # Leaf node, no children
    else:
        raise TypeError("Unknown HDF5 object type: {}".format(type(obj)))

def plot_tree(ax, structure, x, y, dx):
    """Recursively plot the tree structure."""
    node_name, is_group, children = structure
    ax.text(x, y, node_name, ha='center', fontsize=8, weight='bold' if is_group else 'normal')

    if children is not None:
        # Adjust spacing for children
        child_dx = dx / len(children) if len(children) > 0 else dx
        for i, child in enumerate(children):
            child_x = x - dx / 2 + (i + 0.5) * child_dx
            child_y = y - 1.5  # Increased vertical spacing
            ax.plot([x, child_x], [y - 0.1, child_y + 0.1], color='black')
            plot_tree(ax, child, child_x, child_y, child_dx)  # Recurse into children

def visualize_hdf5_structure(filepath):
    """Visualizes the structure of an HDF5 file as a tree."""
    with h5py.File(filepath, 'r') as h5_file:
        structure = get_hdf5_structure('/', h5_file)

    fig, ax = plt.subplots(figsize=(12, 8))  # Adjust size as needed
    ax.axis('off')  # Hide the axis
    plot_tree(ax, structure, 0, 0, 12)  # Starting position and width
    plt.title(f"HDF5 Structure of {filepath}", fontsize=14)
    plt.tight_layout()  # Adjust layout
    plt.show()
    
    
visualize_hdf5_structure(filename)