from engine.saver.base_saver import BaseSaver
from engine.saver.pillow_provider import PillowProvider

import datetime


class ConstructorSaver(BaseSaver):

	def process(self):
		ns = self.get_name_spaces()
		src = self.ctx.SCENE["TempFile"]

		out_s = ns['s']
		out_b = ns['b']
		out_xs = ns['xs']

		res_s = self.ctx.SCENE['Resolution']['Small']
		res_b = self.ctx.SCENE['Resolution']['Big']
		res_xs = self.ctx.SCENE['Resolution']['XSmall']

		PillowProvider.save_image(src, out_s, res_s)
		PillowProvider.save_image(src, out_b, res_b)
		PillowProvider.save_image(src, out_xs, res_xs)

	def get_name_spaces(self):
		return {
			"xs": str.format("{0}/{1}/{2}_{3}.png", self.root, self.subfold, self.file, 'xs').lower(),
			"s": str.format("{0}/{1}/{2}_{3}.png", self.root, self.subfold, self.file, 's').lower(),
			"b": str.format("{0}/{1}/{2}_{3}.png", self.root, self.subfold, self.file, 'b').lower()
		}

	def set_paths(self, detail, model):
		self.root = self.root
		self.subfold = detail['file_id']
		self.file = "{0}_{1}".format(detail['file_id'], model)
