import datetime
import os
import json

from PIL import Image


class ProcessHelper:

	@staticmethod
	def get_folder_name(root, args):
		dt = datetime.datetime.now()
		if args.version is not None:
			pt = root + "/" + args.version
		else:
			pt = root + "/" + dt.strftime("%d_%b_%Y")
		return pt

	@staticmethod
	def make_folder_by_detail(path):
		lower_path = path.lower()
		if not os.path.exists(lower_path):
			os.makedirs(lower_path)

	@staticmethod
	def get_meterial_name(raw):
		spl = raw.split('.')
		if len(spl) > 0:
			return spl[0].strip()
		return raw.strip()

	@staticmethod
	def write_stats(path, entity):
		data_path = str.format("{0}/.dat", path)
		json_data = ProcessHelper.read_json(data_path)
		json_data[entity] = 'ok'
		ProcessHelper.write_json(data_path, json_data)

	@staticmethod
	def check_entity(path, entity):
		data_path = str.format("{0}/.dat", path)
		json_data = ProcessHelper.read_json(data_path)
		if entity in json_data:
			return False
		else:
			return True

	@staticmethod
	def read_dat_file(path):
		return ProcessHelper.read_json(str.format("{0}/.dat", path))

	@staticmethod
	def read_json(path):
		try:
			if os.path.exists(path) == False:
				ProcessHelper.write_json(path, dict(), False)

			with open(path, mode='r') as f:
				data = f.read()
				return json.loads(data)

		except OSError:
			print("Creation of the directory %s failed" % path)

	@staticmethod
	def write_json(file, data, close=True):
		with open(file, mode="w+") as f:
			f.write(json.dumps(data, indent=4))
			if close:
				f.close()
