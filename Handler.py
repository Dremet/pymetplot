#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Github: https://github.com/Dremet/pymetplot  #
################################################

import os

from Model import *


import config_models  as mcfg
import config_handler as hcfg

# setting time zone
os.environ['TZ'] = 'UTC'

# ––– CLASS DEFINITION –––

class Handler():
	def __init__(self):
		self.models = []

		for model in mcfg.models:
			self.models.append(mcfg.model_classes[model](name = model, **mcfg.props[model]))

		os.chdir(hcfg.main_dir)
		os.environ['PWD'] = os.getcwd()

	def run(self):

		pass




if __name__ == "__main__":
	handler = Handler()
	handler.run()