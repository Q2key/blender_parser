from abc import ABC, abstractmethod
import datetime

class BaseSaver(ABC):

	def __init__(self, ctx, args):
		self.ctx = ctx
		self.args = args

	@abstractmethod
	def process(self):
		pass

	@abstractmethod
	def get_name_spaces(self):
		pass

	def get_folder_name(self):
		dt = datetime.datetime.now()
		if self.args.version is not None:
			pt = self.ctx.RENDERS_PATH + "/" + self.args.version
		else:
			pt = self.ctx.RENDERS_PATH + "/" + dt.strftime("%d_%b_%Y")
		return pt
