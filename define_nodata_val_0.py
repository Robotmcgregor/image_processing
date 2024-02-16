#!/usr/bin/env python

"""
This script will imput a raster image and change the values <= 0.52m to a value of zero

Author: Grant Staben
email: Grant.Staben@ntg.gov.au
Date:14/10/2017
"""

# import the modules
import sys
import os
import argparse
import pdb
import numpy as np 
from rios import applier, fileinfo


def getCmdargs():

    p = argparse.ArgumentParser()

    
    p.add_argument("-i","--inimage", help="input seasonal fractional cover image to process")
    
    p.add_argument("-o","--output", help="directroy path and name of the output image")
    
    p.add_argument("-b","--band", default= 0 ,help="input band to produce density slice from. options;0 = bare soil this is default, 1 = pv fraction, 2 = npv fraction (default is %(default)s)")
    
    cmdargs = p.parse_args()
    
    if cmdargs.inimage is None:

        p.print_help()

        sys.exit()

    return cmdargs



def mainRoutine():
    
    cmdargs = getCmdargs()
    
    infiles = applier.FilenameAssociations()
    outfiles = applier.FilenameAssociations()
    otherargs = applier.OtherInputs()
    
    infiles.seasComp = cmdargs.inimage
    outfiles.ds = cmdargs.output
    otherargs.b = cmdargs.band
   
    controls = applier.ApplierControls()
    controls.setOutputDriverName('GTiff')
    options = ['COMPRESS=LZW', 'BIGTIFF=YES', 'TILED=YES', 'INTERLEAVE=BAND','BLOCKXSIZE=256','BLOCKYSIZE=256']
    controls.setCreationOptions(options)
    controls.setWindowXsize(256)
    controls.setWindowYsize(256)
    #controls.setStatsIgnore(0)
    #controls.setReferenceImage(infiles.seasComp)
    
    

    applier.apply(densitySlice, infiles, outfiles, otherargs,controls=controls)  



def densitySlice(info, inputs, outputs, otherargs):
    
    """
    
    function to convert values below 0.52m and above 50m in the lidar canopy height value to nodata  
    
    """
    sc10 = np.array(inputs.seasComp[otherargs.b])
    sc10[sc10 <= 0] = 0.0
    #sc10[sc10 >= 10.000001] = 0
    
    
    
    # for defining the srtm dem and derived products nodata value
    #sc10[sc10 == np.nan] = -9999.0
        
    output = np.array([sc10],dtype=np.float32)
    
        
    outputs.ds = output


    
if __name__ == "__main__":
    mainRoutine()