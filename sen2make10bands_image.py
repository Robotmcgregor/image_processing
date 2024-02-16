#!/usr/bin/env python
"""
A script to blend all the 10 and 20m stacks of Sentinel-2 bands into a single
10m stack, it has been modified from Neils qv_sen2makeTM10.py script which only using just the bands which correspond to the Landsat TM bands. 
This produces an image using B02, B03, B04, B08, B05, B06, B07, B08A, B11, B12 from the original Sentinel-2 band names 

"""
from __future__ import print_function, division

import sys
import os
import argparse

import numpy
from osgeo import gdal

from rios import applier
from rios import fileinfo

import pdb

def getCmdargs():
    """
    Get commandline arguments
    """
    p = argparse.ArgumentParser(description="""
        Create a single stack of Sentinel-2 bands, all at 10m pixel size. Output is a single stack of 10 layers. 
        Bands are out out put as  B1','B2','B3','B4','B5','B6','B7','B8','B9','B10 which is the Sentinel-2 band numbers 
        B02, B03, B04, B08, B05, B06, B07, B08A, B11, B12. 
    """)
    p.add_argument("--ref10", help="Name of 10m input file. Expected to have exactly 4 bands.")
    p.add_argument("--ref20", help="Name of 20m input file.")
    p.add_argument("--outfile", help="Name of output image file")
    cmdargs = p.parse_args()
    
    if cmdargs.ref10 is None:
        p.print_help()
        sys.exit()
    
    return cmdargs


def mainRoutine():
    """
    Main routine
    """
    cmdargs = getCmdargs()
    
       
    infiles = applier.FilenameAssociations()
    outfiles = applier.FilenameAssociations()
    controls = applier.ApplierControls()
    otherargs = applier.OtherInputs()
    
    infiles.ref10 = cmdargs.ref10
    infiles.ref20 = cmdargs.ref20
    outfiles.outimg = cmdargs.outfile
    ref10info = fileinfo.ImageInfo(cmdargs.ref10)
    ref20info = fileinfo.ImageInfo(cmdargs.ref20)
    otherargs.ref10null = ref10info.nodataval[0]
    otherargs.ref20null = ref20info.nodataval[0]

    controls.setResampleMethod('cubic')
    controls.setReferenceImage(cmdargs.ref10)
    controls.setStatsIgnore(otherargs.ref10null)
    
    applier.apply(doMerge, infiles, outfiles, otherargs, controls=controls)
    


def doMerge(info, inputs, outputs, otherargs):
    """
    Merge the 10 and 20m bands
    """
    ref10 = inputs.ref10
    ref20 = inputs.ref20
    
    outputs.outimg = numpy.vstack((ref10, ref20))



def copyScaling(cmdargs): 
    """
    Set layer names. 
    """
    
    # Set explicit layer names 1 to 10
    layerNames = ['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10']
    ds = gdal.Open(cmdargs.outfile, gdal.GA_Update)
    for i in range(10):
        band = ds.GetRasterBand(i+1)
        band.SetDescription(layerNames[i])
   
    del ds


if __name__ == "__main__":
    mainRoutine()