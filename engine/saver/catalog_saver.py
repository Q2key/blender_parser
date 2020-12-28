from helpers.process_helper import ProcessHelper
from engine.saver.base_saver import BaseSaver
from engine.saver.pillow_provider import PillowProvider

import datetime


class CatalogSaver(BaseSaver):

	def process(self):
		ns = self.get_name_spaces()
		src = self.ctx.SCENE["TempFile"]

		out_s = ns['s']
		out_b = ns['b']
		
		res_s = self.ctx.SCENE['Resolution']['Small']
		res_b = self.ctx.SCENE['Resolution']['Big']

		PillowProvider.save_image(src, out_s, res_s)
		PillowProvider.save_image(src, out_b, res_b)

	def get_name_spaces(self):
		return {
			"s": str.format(
				"{0}/{1}/{2}-{3}-s.png",
				self.part_1,
				self.part_2,
				self.part_3,
				self.part_4
				).lower(), 
			"b": str.format(
				"{0}/{1}/{2}-{3}-b.png",
				self.part_1,
				self.part_2,
				self.part_3,
				self.part_4
				).lower()
		}

	def set_paths(self, detail, model):
		self.part_1 = self.get_folder_name()
		self.part_2 = detail['file_id']
		self.part_3 = model
		self.part_4 = detail['preset_id']
