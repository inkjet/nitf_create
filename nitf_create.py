# -*- coding: utf-8 -*-
"""
Sample 16-bit PNG to NITF creation while folding in RPC info
Requires GDAL and ImageMagick to be installed

Input: <file_name.png>     - 16-bit input image
       <file_name_rpc.txt> - Text file of RPC values

@author: srodkey
"""
import os

# Sample 16-bit input image from http://www.brucelindbloom.com/index.html?ReferenceImages.html
input_file = '16_bit.png'
temp_im_file = os.path.splitext(input_file)[0] + '_to_8_bit.tif'
first_geotiff = os.path.splitext(input_file)[0] + '.tif'
second_geotiff = os.path.splitext(input_file)[0] + '_geo2.tif'
nitf_name = os.path.splitext(input_file)[0] + '_output.ntf'

# do simple 16- to 8-bit conversion - can get much fancier with Imagemagick
im_cmd = 'convert ' + input_file + ' -depth 8 -type grayscale ' + temp_im_file
print "Running command: " + im_cmd
os.system(im_cmd)

# Now on to the fun stuff:
# First, From the GDAL documentation for NITFs: "No support for writing RPCs for now."
# But... regarding GeoTIFFs: "Support writing RPC TIFF tag" (https://trac.osgeo.org/gdal/wiki/rfc22_rpc)

# To insert RPCs into a GeoTIFF, GDAL looks for an file named "<filename>_rpc.txt" in the same directory as the file
# to be converted. But the documentation doesn't provide any info on what that file should look like. I randomly came
# across one at this site that appears to work:
# https://git.earthdata.nasa.gov/projects/GEE/repos/gdal-enhancements-for-esdis/browse/autotest/gcore/data/test_rpc.txt)
gdal_cmd = 'gdal_translate -of GTiff ' + temp_im_file + ' ' + first_geotiff
print "Running command: " + gdal_cmd
os.system(gdal_cmd)

# Oddly, two intermediate geotiffs need to be made - the first is relies on the external rpc.txt file, then the second
# one writes them to the GeoTIFF metadata after gdal_translate is called
gdal_cmd = 'gdal_translate -of GTiff ' + first_geotiff + ' ' + second_geotiff
print "Running command: " + gdal_cmd
os.system(gdal_cmd)

gdal_cmd = 'gdal_translate -of NITF ' + second_geotiff + ' ' + nitf_name
print "Running command: " + gdal_cmd
os.system(gdal_cmd)

# You can now test the presence of RPCs by running "gdalinfo <nitf_file>"

# Clean up temp files
os.remove(temp_im_file)
os.remove(first_geotiff)
os.remove(second_geotiff)
os.remove(nitf_name + '.aux.xml') #intermediate GDAL file containing RPCs from NITF creation