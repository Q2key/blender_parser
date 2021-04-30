import datetime
import os
import json

class ProcessHelper:

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
		path = path.lower()
		try:
			if os.path.exists(path) == False:
				ProcessHelper.write_json(path, dict(), False)

			with open(path, mode='r') as f:
				data = f.read()
				return json.loads(data)

		except OSError:
			pass
			#print("Creation of the directory %s failed" % path)

	@staticmethod
	def write_json(file, data, close=True):
		file = file.lower()
		try:
			with open(file, mode="w+") as f:
				f.write(json.dumps(data, indent=4))
				if close:
					f.close()
		except Exception as inst:
			print(inst)
			
			
