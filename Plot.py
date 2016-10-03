#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

import pickle
import subprocess as sp

import config_plot as pcfg

# ––– CLASS DEFINITIONS –––

class Plot(Basemap):
    def __init__(self, basemapParams):
        super().__init__(**basemapParams)
        self.layers = []


    def addLayer(self, layer):
        self.layers.append(layer)

    def plot(self, data, title, title_fontsize, filename):
        fig = plt.figure(figsize=pcfg.fig_size)
        
        for layer in self.layers:
            if isinstance(layer, SourceLayer):
                fig = layer.plot(self, fig)
            else:
                layer.plot(self, data)
        
        plt.title(title, fontsize = title_fontsize)
        
        plt.savefig(pcfg.plt_dir+filename, bbox_inches=pcfg.bbox_inches, transparent = pcfg.transparent)
        
        plt.close('all')



if __name__ == '__main__':
	# create directory for current plots
	sp.call(["mkdir", "-p", pcfg.plt_dir])

	region = "eu"

	plot = Plot({
			"projection":"lcc",
			"resolution": pcfg.resolution,
			"rsphere":(6378137.00,6356752.3142), 
			"area_thresh": 1000., 
			"llcrnrlon":pcfg.coords_map[region][2],
			"llcrnrlat":pcfg.coords_map[region][0],
			"urcrnrlon":pcfg.coords_map[region][3],
			"urcrnrlat":pcfg.coords_map[region][1],
			"lon_0":
				(pcfg.coords_map[region][2]+pcfg.coords_map[region][3])/2.,
			"lat_0":
				(pcfg.coords_map[region][0]+pcfg.coords_map[region][1])/2.
			})

	plot.plot("", "Test", 18, "test.png")
	#m = Basemap(width=920000,height=1100000,resolution='f',projection='tmerc',lon_0=-4.2,lat_0=54.6)
	#pickle.dump(m,open('map.pickle','wb'),-1)
	#m2 = pickle.load(open('map.pickle','rb'))