import datetime
import os
import json

import time


class FileHelper:

    def open_file(self, path):
        with open(path, mode="w+") as f:
            self.file = f

    def close_file(self):
        if self.file.closed == False:
            self.file.close()

    def get_file(self):
        return self.file