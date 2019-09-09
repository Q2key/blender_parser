import os
import json
from helpers.process_helper import ProcessHelper


class InstallCommand:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    def run(self):
        self.init_details()

    def init_details(self):
        pass

