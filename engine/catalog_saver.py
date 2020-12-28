from helpers.process_helper import ProcessHelper

class CatalogSaver:
	def __init__(self, src, result, cfg_sizes):
		self.sizes = sizes
		self.src = src
		self.result = result

	def process(self):
		ProcessHelper.save_image(self.src, self.result, self.sizes)