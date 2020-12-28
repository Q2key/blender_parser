from abc import ABC, abstractmethod
import datetime
from helpers.directory_helper import DirectoryHelper

class BaseSaver(ABC):

	def __init__(self, ctx, args):
		self.ctx = ctx
		self.args = args
		self.root = DirectoryHelper.get_root_folder(self.ctx.RENDERS_PATH, args) 

	@abstractmethod
	def process(self):
		pass

	@abstractmethod
	def get_name_spaces(self):
		pass