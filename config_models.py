#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################

from Model import *


#--- setting model properties ---
# class       -> class name (see Model.py)
# init_time   -> "latest" or date in format "YYYYMMDD_HH"
# data_source -> "link" or "directory"
# link        -> may be empty of data_source is "directory"
# link_alt    -> alternative source on the internet (may be empty!)
# directory   -> may be empty of data_source is "link"

prop  = {
			"GFS" : 
				{
					"class"       : GFS,      
					"init_time"   : "latest", 
					"data_source" : "link",   
					"link"        : "ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",  
					"link_alt"    : "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/",  
					"directory"   : "",  
				},
			
			"ICON" : 
				{
					"class"       : ICON,
					"init_time"   : "latest",
					"data_source" : "link",
					"link"        : "",
					"link_alt"    : "",
					"directory"   : "",
				}
		}

# model classes
model_classes = {"GFS" : GFS, "ICON" : ICON}

# "latest" or date in format "YYYYMMDD_HH"
init_time = {"GFS" : "latest", "ICON" : "latest"}

# which o
models = ["GFS", "ICON"]

