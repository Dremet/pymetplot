#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

import pickle
import subprocess as sp
from abc import ABCMeta, abstractmethod

from netCDF4 import Dataset

import mpl_util

import config_plot as pcfg

# setting time zone
os.environ['TZ'] = 'UTC'



# ––– CLASS DEFINITIONS –––

class Plot(Basemap):
	def __init__(self, basemapParams):
		super().__init__(**basemapParams)
		self.layers = []


	def addLayer(self, layer):
		"""
		Adds given layer
		"""
		self.layers.append(layer)

	def plot(self, data, title, title_fontsize, filename):
		"""
		Creates figure and plots all layers on it.
		"""
		fig = plt.figure(figsize=pcfg.fig_size)
		
		for layer in self.layers:
			if isinstance(layer, SourceLayer):
				fig = layer.plot(self, fig)
			else:
				layer.plot(self, data)
		
		plt.title(title, fontsize = title_fontsize)
		
		plt.savefig(pcfg.plt_dir+filename, bbox_inches=pcfg.bbox_inches, transparent = pcfg.transparent)
		
		plt.close('all')

class Layer(metaclass=ABCMeta):
	def __init__(self):
		pass
	
	@abstractmethod
	def plot(self, plot, data):
		return NotImplemented

class BackgroundLayer(Layer):
	def __init__(self, bgtype, coords):
		#possible bgtype values: "borders", "topo", "both"
		self.bgtype = bgtype
		self.lonStart = coords[0]
		self.lonEnd   = coords[1]
		self.latStart = coords[2]
		self.latEnd   = coords[3]
	
	def plot(self, plot, data):
		if self.bgtype == "borders" or self.bgtype == "both":
			# draw coastlines, country boundaries, fill continents.
			plot.drawcoastlines(linewidth=0.25)
			plot.drawcountries(linewidth=0.25)
			#plot.fillcontinents(color='white',lake_color='white')
			# draw the edge of the map projection region (the projection limb)
			plot.drawmapboundary(fill_color='white')
			# draw lat/lon grid lines every 30 degrees.
			plot.drawmeridians(np.arange(0,360,30))
			plot.drawparallels(np.arange(-90,90,30))
		if self.bgtype == "topo" or self.bgtype == "both":
			
			# https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/ice_surface/grid_registered/netcdf/
			etopo1name='ETOPO1_Ice_g_gmt4.grd'
			#levels=[0,0.0001,0.0002,.0003,.0004,.0005,.0006,.0007,.0008,.0009,.0010,.0011,.0012,.0013,.0014,.0015,.0016,
			#		50,75,100,150,200,250,300,400,500,625,750,1000,1250,1500,1750,2000,2250,2500,4000]
			levels=[0,50,200,400,600,800,1000,1250,1500,1750,2000,2250,2500,3000]
			etopo1 = Dataset(etopo1name,'r')
			
			lons = etopo1.variables["x"][:]
			lats = etopo1.variables["y"][:]
			
			res = self.findSubsetIndices(self.latStart-5,self.latEnd+5+30,self.lonStart-70,self.lonEnd+10,lats,lons)
			
			lon,lat=np.meshgrid(lons[res[0]:res[1]],lats[res[2]:res[3]])    
			#print ("Extracted data for area %s : (%s,%s) to (%s,%s)"%(name,lon.min(),lat.min(),lon.max(),lat.max()))
			bathy = etopo1.variables["z"][int(res[2]):int(res[3]),int(res[0]):int(res[1])]
			bathySmoothed = bathy #laplaceFilter.laplace_filter(bathy,M=None)
			
			if self.lonStart < 0 and self.lonEnd < 0:
				lon_0= - (abs(self.lonEnd)+abs(self.lonStart))/2.0
			else:
				lon_0=(abs(self.lonEnd)+abs(self.lonStart))/2.0
			
			x, y = plot(lon,lat)
			
			plot.drawlsmask(land_color='#0fc64f', ocean_color='#2BBBFF',resolution='h',lakes=True,grid=1.25)
			plot.drawmeridians(np.arange(lons.min(),lons.max(),5),labels=[0,0,0,1])
			plot.drawparallels(np.arange(lats.min(),lats.max(),2),labels=[1,0,0,0])	

			
			import matplotlib.colors as colors

			def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
				new_cmap = colors.LinearSegmentedColormap.from_list(
					'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
					cmap(np.linspace(minval, maxval, n)))
				return new_cmap

			
			#plt.cm.gist_earth
			cmap = plt.get_cmap('terrain')
			new_cmap = truncate_colormap(cmap, 0.25, 1.0)

			CS1 = plot.contourf(x,y,bathySmoothed,levels,
					cmap=new_cmap,#mpl_util.LevelColormap(levels,cmap=),
					extend='max',
					alpha=1.0,
					origin='lower')

			cbar = plt.colorbar(CS1, orientation = "horizontal", fraction=0.046, pad=0.04, aspect=30, shrink=0.67)

			CS1.axis='tight'
		
	
	def findSubsetIndices(self,min_lat,max_lat,min_lon,max_lon,lats,lons):
		""" CREDITS: http://www.trondkristiansen.com/?page_id=846
					 https://github.com/trondkr 
		"""
		"""Array to store the results returned from the function"""
		res=np.zeros((4),dtype=np.float64)
		minLon=min_lon; maxLon=max_lon
		
		distances1 = []; distances2 = []
		indices=[]; index=1
		
		for point in lats:
			s1 = max_lat-point # (vector subtract)
			s2 = min_lat-point # (vector subtract)
			distances1.append((np.dot(s1, s1), point, index))
			distances2.append((np.dot(s2, s2), point, index-1))
			index=index+1
			
		distances1.sort()
		distances2.sort()
		indices.append(distances1[0])
		indices.append(distances2[0])
		
		distances1 = []; distances2 = []; index=1
	   
		for point in lons:
			s1 = maxLon-point # (vector subtract)
			s2 = minLon-point # (vector subtract)
			distances1.append((np.dot(s1, s1), point, index))
			distances2.append((np.dot(s2, s2), point, index-1))
			index=index+1
			
		distances1.sort()
		distances2.sort()
		indices.append(distances1[0])
		indices.append(distances2[0])
		
		""" Save final product: max_lat_indices,min_lat_indices,max_lon_indices,min_lon_indices"""
		minJ=indices[1][2]
		maxJ=indices[0][2]
		minI=indices[3][2]
		maxI=indices[2][2]
		
		res[0]=minI; res[1]=maxI; res[2]=minJ; res[3]=maxJ;
		return res

class SourceLayer(Layer):
	def __init__(self, region, model, run, valid, hours, day):
		self.region = region
		self.model  = model
		self.run    = run
		self.valid  = valid
		self.hours  = hours
		self.day    = day
	
	def plot(self, plot, fig):
		if self.region == "ger":
			fig.text(0.348,0.199,'©wetterquelle.de',fontsize=20,
					ha='center',va='top',color='k',
					bbox={'boxstyle':'round','facecolor':'white', 'alpha':0.9})
			
			fig.text(0.363,0.159, self.model+' RUN: ' + self.run + 'UTC',fontsize=15,
					ha='center',va='top',color='k')
			
			fig.text(0.630,0.159, 'VAL: ' + self.day + ', ' + self.valid + 'UTC (+' + self.hours + 'h)',fontsize=15,
					ha='center',va='top',color='k')
		else:
			fig.text(0.218,0.199,'©wetterquelle.de',fontsize=20,
					ha='center',va='top',color='k',
					bbox={'boxstyle':'round','facecolor':'white', 'alpha':0.9})
			
			fig.text(0.240,0.159, self.model+' RUN: ' + self.run + 'UTC',fontsize=16,
					ha='center',va='top',color='k')
			
			fig.text(0.737,0.159, 'VALID: ' + self.day + ', ' + self.valid + 'UTC (+' + self.hours + 'h)',fontsize=16,
					ha='center',va='top',color='k')
		
		return fig


if __name__ == '__main__':
	# create directory for current plots
	sp.call(["mkdir", "-p", pcfg.plt_dir])

	region = "eu"

	plot = Plot({
			"projection":"lcc",
			"resolution": pcfg.resolution,
			"rsphere":(6378137.00,6356752.3142), 
			#"area_thresh": 1.,  # https://github.com/matplotlib/basemap/issues/158
			"llcrnrlon":pcfg.coords_map[region][2],
			"llcrnrlat":pcfg.coords_map[region][0],
			"urcrnrlon":pcfg.coords_map[region][3],
			"urcrnrlat":pcfg.coords_map[region][1],
			"lon_0":
				(pcfg.coords_map[region][2]+pcfg.coords_map[region][3])/2.,
			"lat_0":
				(pcfg.coords_map[region][0]+pcfg.coords_map[region][1])/2.
			})

	plot.addLayer(BackgroundLayer("both", pcfg.coords_map[region]))
	#plot.addLayer(SourceLayer("eu", "GFS", "2016-10-03 00:00Z", "2016-10-03 00:00Z", "00", "Mon"))
	plot.plot("", "Topography [m]", 18, "topo_eu.png")
	#m = Basemap(width=920000,height=1100000,resolution='f',projection='tmerc',lon_0=-4.2,lat_0=54.6)
	#pickle.dump(m,open('map.pickle','wb'),-1)
	#m2 = pickle.load(open('map.pickle','rb'))