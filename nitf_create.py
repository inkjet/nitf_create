#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 13:03:22 2018

@author: srodkey
"""
import os

# Sample image from http://www.brucelindbloom.com/index.html?ReferenceImages.html
input_file = 'DeltaE_16bit_gamma1.0.tif'
temp_file = os.path.splitext(input_file)[0] + '_8_bit.tif'
nitf_name = os.path.splitext(input_file)[0] + '.ntf'

os.system('convert ' + input_file + ' -depth 8 -type grayscale ' + temp_file)

os.system('gdal_translate ' + temp_file + ' -of NITF ' + nitf_name)