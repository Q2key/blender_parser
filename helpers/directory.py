import datetime
import os
import json

class DirectoryHelper:

	@staticmethod
	def get_root_folder(root, args):
		dt = datetime.datetime.now()
		if args.version is not None:
			pt = root + "/" + args.version
		else:
			pt = root + "/" + dt.strftime("%d_%b_%Y_%S")
		return pt

	@staticmethod
	def make_folder_by_detail(path):
		lower_path = path.lower()
		if not os.path.exists(lower_path):
			os.makedirs(lower_path)
