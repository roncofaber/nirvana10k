"""
Read module for nirvana10k

Contains functions for reading and parsing HDF5 files from Nirvana instrument.
"""

from .h5tosample import h5_to_samples

__all__ = ["h5_to_samples"]