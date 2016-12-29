#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################

import os
import subprocess as sp
import numpy.ma as ma
from datetime import datetime, timedelta
from time import strftime,sleep

# setting time zone
os.environ['TZ'] = 'UTC'

# ––– CLASS DEFINITION –––

# Atmospheric Model #
class Model():
	def __init__(self, init_time, fcst_hours, data_source, source_link, source_link_alt, source_dir, **unused_props):
		
		if init_time != "latest":
			# comes in format "YYYYMMDD_HH"
			self.init = datetime.strptime(init_time, "%Y%m%d_%H")
		else:
			self.init = self.getLatestInitTime()
		
		self.fcst_hours      = fcst_hours
		self.data_source     = data_source
		self.source_link     = source_link
		self.source_link_alt = source_link_alt
		self.source_dir      = source_dir

		self.initOutputTimesteps()


	def initOutputTimesteps(self):
		"""
		Initialize output Timestep by creating instances of them and saving them to self.output_timesteps
		"""
		self.output_timesteps = []

		for fcst_hour in self.fcst_hours:
			if fcst_hour == 0:
				self.output_timesteps.append(InitOutputTimestep(self))
			else:
				self.output_timesteps.append(FcstOutputTimestep(self, fcst_hour))

	def getDataFiles(self):
		"""
		Downloads (or copies) files.
		"""

		for output_timestep in self.output_timesteps:
			output_timestep.getDataFile()


# Global Forecast System #
# https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs #
class GFS(Model):
	def __init__(self, name, **props):
		self.name = "GFS"
		super().__init__(**props)

	def getLatestInitTime(self):
		"""
		Returns datetime object of last model run of which data should already be available or will be available soon (<1hour).
		
		"""

		current_hour = int(strftime("%H"))
		
		# calculating how many hours ago the model run started
		if current_hour in [0,1]:
			runhour = 18
		else:
			runhour = int(ma.floor((current_hour-2)/6.0)*6)

		if runhour == 18 and current_hour in [0,1,2]:
			hours_ago = (current_hour+24)-18
		else:
			hours_ago = current_hour-runhour

		
		# saving datetime object with information on when the model started running
		run_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours = hours_ago)

		return run_time

	def getFullDownloadLink(self, forecast_hour):
		"""
		Provides full download path for given forecast hour.

		"""

		# get init time as string
		model_init_str = self.init.strftime("%Y%m%d%H")

		# create folder and file name
		foldername = 'gfs.' + model_init_str
		filename   = 'gfs.t' + model_init_str[-2:] + 'z.pgrb2.0p25.f' + '{0:0>3}'.format(forecast_hour)
		
		# put all parts together in order to create the full download path
		# if given this is also done for alternative link
		return (self.source_link + foldername + '/' + filename, self.source_link_alt + foldername + '/' + filename if len(self.source_link_alt) > 0 else "")


# ICON (Icosahedral non-hydrostatic) general circulation model #
# http://www.mpimet.mpg.de/en/science/models/icon/ #
class ICON(Model):
	def __init__(self, name, **props):
		self.name = "ICON"
		super().__init__(**props)
	def getLatestInitTime(self):
		"""
		
		"""
		pass

	def getDataFiles(self):
		"""

		"""

		pass


# Output Timestep #
class OutputTimestep():
	def __init__(self, model, forecast_hour):
		self.forecast_hour = forecast_hour
		self.model         = model

	def getDataFile(self):
		
		if self.model.data_source == "link":
			
			link, alt_link = self.model.getFullDownloadLink(self.forecast_hour)

			downloaded = 0

			while not downloaded == 1:
				try:
					# try primary link
					sp.check_call(["wget", "-O", link.split("/")[-1] + ".grb", link])
					
					downloaded = 1
					
				except sp.CalledProcessError:
					# alternative download source given? let's give it a try
					if len(alt_link) > 0:
						try:
							sp.check_call(["wget", "-O", alt_link.split("/")[-1] + ".grb", alt_link])
							
							downloaded = 1
							
						except sp.CalledProcessError:
							# file not available at the servers, so checking again in 15 seconds
							
							sleep(15)
					else:
						sleep(15)
								
		else:
			raise NotImplementedError("Currently not implemented to get data files from somewhere else than ftp/http.")


# Initialization Output Timestep #
class InitOutputTimestep(OutputTimestep):
	def __init__(self, model):
		super().__init__(model, 0)


# Forecast Output Timestep # 
class FcstOutputTimestep(OutputTimestep):
	def __init__(self, model, forecast_hour):
		super().__init__(model, forecast_hour)