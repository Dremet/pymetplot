#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################





# ––– CLASS DEFINITION –––


class Model():
	def __init__(self, init_time):
		self.init = init_time
		

class GFS(Model):
	def __init__(self, name, init_time):
		self.name = "GFS"
		super().__init__(init_time)

class ICON(Model):
	def __init__(self, name, init_time):
		self.name = "ICON"
		super().__init__(init_time)

