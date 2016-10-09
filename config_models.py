#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################

from Model import *
import numpy as np

# create plots of following models
models = ["GFS", "ICON"]


# model classes
model_classes = {"GFS" : GFS, "ICON" : ICON}

#--- setting model properties ---
# class           -> class name (see Model.py)
# init_time       -> "latest" or date in format "YYYYMMDD_HH"
# fcst_hours      -> iterable with forecast hours
# data_source     -> "link" or "dir"
# source_link     -> may be empty of data_source is "dir"
# source_link_alt -> alternative source on the internet (may be empty!)
# source_dir      -> may be empty of data_source is "link"

props = {
	"GFS" : 
	{
		"class"           : GFS,      
		"init_time"       : "latest", 
		"fcst_hours"      : np.arange(0,6,3),
		"data_source"     : "link",
		"source_link"     : "ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",  
		"source_link_alt" : "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/",  
		"source_dir"      : "",  
	},
	
	"ICON" : 
	{
		"class"           : ICON,
		"init_time"       : "20161009_00",
		"fcst_hours"      : np.arange(0,6,3),
		"data_source"     : "link",
		"source_link"     : "",
		"source_link_alt" : "",
		"source_dir"      : "",
	}
}






