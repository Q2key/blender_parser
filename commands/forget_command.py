import os
import json
from helpers.process import ProcessHelper


class ForgetCommand:

	def __init__(self, ctx, args):
		self.ctx = ctx
		self.args = args
		self.scan_path = self.ctx.RENDERS_PATH + "/" + self.args.version 

	def dir_walk(self, path):
		for root, dirs, files in os.walk(path):
			path = root.split(os.sep)
			for file in files:
				if ".dat" in file:
					dat_path = root + "/" + file
					dat_dict = ProcessHelper.read_json(dat_path)
					for key in self.args.entity:					
						try:
							dat_dict.pop(key, None)
						except KeyError as ex:
							pass
					
						ProcessHelper.write_json(dat_path, dat_dict, True)
							



	def run(self):
		self.dir_walk(self.scan_path)
