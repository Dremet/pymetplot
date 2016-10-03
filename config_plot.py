#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################

# plot directory
plt_dir = "plots/"

# figure size
fig_size = (14,12)

# saving options matplotlib
bbox_inches ='tight'
transparent = False



# coords for basemap plot
coords_map = {"eu" : [22.,70.,-25.,57.], "ger" : [46.,56.,4.,17.], "nger" : []} 
# coords for grib data (generally needs to be wider than coords_map) !!! NO NEGATIVE LONS HERE !!!
coords_data = {"eu" : [24,75,295,57], "ger" : [20,60,355,25]}

# resolution for basemap, "h" = high
resolution = "h"