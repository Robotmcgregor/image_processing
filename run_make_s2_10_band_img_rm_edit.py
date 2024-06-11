#!/usr/bin/env python
"""
this script runs the image sen2make10bands_image.py script, this enables the script to be run from in a notebook on windows system  
Author: Grant Staben
Date: 24/01/2020

Updated: Rob McGregor
Date: 28/10/2021

"""
from __future__ import print_function, division

# import the requried modules
import sys
import os
import argparse
import pdb
import pandas as pd
import csv
import subprocess
import rasterio
import numpy as np
import shutil
from zipfile import ZipFile
from pyunpack import Archive
from glob import glob


# command arguments 
def getCmdargs():

    """
    Get commandline arguments
    """
    p = argparse.ArgumentParser(description="""
        Create a single stack of Sentinel-2 bands, all at 10m pixel size. Output is a single stack of 10 layers. 
        Bands are out out put as  B1','B2','B3','B4','B5','B6','B7','B8','B9','B10 which is the Sentinel-2 band numbers 
        B02, B03, B04, B08, B05, B06, B07, B08A, B11, B12. 
    """)
    p.add_argument("--directory", help="Enter the directory of the ziped files.")
    p.add_argument("--file_type", help="Enter file extension of compressed package (i.e. zip or 7z.")
    cmdargs = p.parse_args()
    
    if cmdargs.directory is None:
        p.print_help()
        sys.exit()
    
    return cmdargs

def unzip7(directory, file_type):
    #directory = "C:\\Users\\rmcgr\\Desktop\\test_zip"
    #Check for a scratch folder, if one does not exist create one.
    scratchDir = directory + "\\scratch"
    #print(scratchDir)
    check_dir = os.path.isdir(scratchDir)

    if not check_dir:
        os.makedirs(scratchDir)
        print("created: " + scratchDir)
        
    else:
        print(scratchDir + " already exists.")
        
        
    #Unzip files to scratch folder
    for filename in os.listdir(directory):

        if filename.endswith('zip'):
            print('located: ', filename)
            Archive(directory + "\\" + filename).extractall(scratchDir)
            print(filename, " has been unzipped")
        elif filename.endswith('.7z'):
            print('located: ', filename)
            Archive(directory + "\\" + filename).extractall(scratchDir)
            print(filename, " has been unzipped")
        else:
            pass
    
    return scratchDir
                                                     

def runscript(ref10,ref20,outimg):
    
    """
    call the script and run it.
    
    """ 
    print('out_img: ', outimg)
    cmd = "python sen2make10bands_image.py --ref10 %s --ref20 %s --outfile %s"% (ref10,ref20,outimg) 
       
    os.system(cmd)
    print (outimg + ' complete')
    
    
def make_dir(directory):
    check_dir = os.path.exists(directory)
    if check_dir:
        pass
    else:
        os.mkdir(directory)
        print(directory, ' created..')
        
    


def file_images(scratch1):
    
    # ----------------------- refile ------------------------------------
    for file in glob("{0}\\*.img".format(scratch1)):

        print('file: ', file)
        file_list_ = file.rsplit('\\', 1)
        #print('file_name: ', file_name)
        file_name = file_list_[1]

        #print(file_name, ' is a .img file...')

        file_list = file_name.split('_')
        #print('file_list: ', file_list)
        tile_ = file_list[1]
        #print('tile_: ', tile_)
        file_date = file_list[2]
        #print('file_date: ', file_date)

        final_tile = tile_[1:].replace('r', '_')
        #print('final_tile: ', final_tile)


        if str(file_date).startswith('m'):
            file_year = file_date[1:5]
            file_date_ = file_date[1:-6]
            #print('file_date_: ', file_date_)
            #print('file_year mmmm: ', file_year)

        elif str(file_date).startswith('t'):

            print('Script NOT complete')
            import sys
            sys.exit()

        else:
            file_year = file_date[:4]
            file_date_ = file_date[:-2]


        #print('file_date_: ', file_date_)

        tile_dir = 't' + final_tile[:3]
        print(tile_dir)

        tile_dir_dir = os.path.join(r'Z:\Sentinel2', tile_dir)
        print(tile_dir_dir)
        make_dir(tile_dir_dir)

        final_tile_ = 't' + final_tile
        tile_dir = os.path.join(tile_dir_dir, final_tile_)
        print(tile_dir)
        make_dir(tile_dir)
        year_dir = os.path.join(tile_dir, str(file_year))
        print(year_dir)
        make_dir(year_dir)

        date_dir = os.path.join(year_dir, str(file_date[:-2]))
        make_dir(date_dir)
        print(date_dir)


        output__ = '{0}\\{1}'.format(date_dir, file_name)
        if os.path.exists(file):
            shutil.move(file, output__)
            print('-- file: ', file)
            print('--- moved to: ', output__)
            print('-'*100)
            
            
            
def main():
    
    # calls in the command arguments and runscript function. 
    
    cmdargs = getCmdargs()
    directory =cmdargs.directory
    file_type = cmdargs.file_type
    
    scratch_dir = unzip7(directory, file_type)
    print('completed unpack.')
    print('searching for: ', "{0}\\*abam?.img".format(scratch_dir))
                             
    for file in glob("{0}\\*abam?.img".format(scratch_dir)):
        print('-'*50)
        print('file: ', file)
        file_begin = file[:-7]
        #print(file_begin)
        utm = file[-5:-4]
        print(utm)
        #print(file_begin)
        t20 = "{0}_abbm*".format(file_begin)
        #print('t20: ', t20)
        for t20_ in glob(t20):
            print(t20_)

        print('file: ', file)
        path_10m = "{0}".format(file)
        print('path10: ', path_10m)
        path_20m = "{0}bm{1}.img".format(file_begin, utm)
        print('path20: ', path_20m)
        output = "{0}mm{1}.img".format(file_begin, utm)
        print('output: ', output)

        runscript(path_10m, path_20m, output)
        print('-'*50)
        
    file_images(scratch_dir)
    


if __name__ == "__main__":
    main()
    