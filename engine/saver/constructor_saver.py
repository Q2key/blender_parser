from helpers.process_helper import ProcessHelper
from engine.saver.base_saver import BaseSaver
from engine.saver.pillow_provider import PillowProvider

import datetime


class ConstructorSaver(BaseSaver):

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
		s = 's'
		b = 'b'
		l = 'l'
		return {
			"s": str.format("{0}/{1}/{2}_{3}.png", self.root, self.subfold, self.file, s).lower(),
			"b": str.format("{0}/{1}/{2}_{3}.png", self.root, self.subfold, self.file, b).lower(),
			"l": str.format("{0}/{1}/{2}_{3}.png", self.root, self.subfold, self.file, l).lower()
		}

	def set_paths(self, detail, model):
		self.root = self.get_folder_name()
		self.subfold = detail['file_id']
		self.file = "{0}_{1}".format(detail['file_id'], model)