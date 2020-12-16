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

    def write_stats(self, path, entity):
        data_path = str.format("{0}/.dat", path)
        json_data = self.read_json(data_path)
        json_data[entity] = 'ok'
        self.write_json(data_path, json_data)

    def check_entity(self, path, entity):
        data_path = str.format("{0}/.dat", path)
        json_data = self.read_json(data_path)

        if entity in json_data:
            return False
        else:
            return True

    def read_json(self, path):
        try:
            if os.path.exists(path) == False:
                self.write_json(path, dict(), False)

            with open(path, mode='r') as f:
                data = f.read()
                return json.loads(data)

        except OSError:
            print("Creation of the directory %s failed" % path)

    def write_json(self, file, data, close=True):
        self.file.write(json.dumps(data, indent=4))
        if close:
            self.close_file()

    def read_dat_file(self, path):
        return self.read_json(str.format("{0}/.dat", path))
