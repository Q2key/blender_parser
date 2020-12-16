import datetime
import os
from PIL import Image
import json


class ProcessHelper:

    @staticmethod
    def get_folder_name(root):
        dt = datetime.datetime.now()
        ft = dt.strftime("%d_%b_%Y")
        pt = root + "/" + ft
        return pt

    @staticmethod
    def get_image_name(root, subfold, file, res):
        s = 's'
        b = 'b'
        l = 'l'
        return {
            "s": str.format("{0}/{1}/{2}_{3}.png", root, subfold, file, s),
            "b": str.format("{0}/{1}/{2}_{3}.png", root, subfold, file, b),
            "l": str.format("{0}/{1}/{2}_{3}.png", root, subfold, file, l)
        }

    @staticmethod
    def make_folder_by_detail(detail_code):
        pass

    @staticmethod
    def get_meterial_name(raw):
        spl = raw.split('.')
        if len(spl) > 0:
            return spl[0].strip()
        return raw.strip()

    @staticmethod
    def save_big(ns, res):
        img = Image.open(ns['l'])
        new_width = res["Big"]["x"]
        new_height = res["Big"]["y"]
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(ns['b'])

    @staticmethod
    def save_small(ns, res):
        img = Image.open(ns['b'])
        new_width = res["Small"]["x"]
        new_height = res["Small"]["y"]
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(ns['s'])

    @staticmethod
    def get_camel(raw):
        cml = ''
        spl = raw.split('_')
        cml_array = []
        for i in range(len(spl)):
            s = spl[i]
            if i > 0:
                l = s[:1].upper()
                s = s[:0] + l + s[1:]
            cml_array.append(s)
        return "".join(cml_array)

    @staticmethod
    def hex2col(hex, normalize=False, precision=None):
        col = []
        it = iter(hex)
        for char in it:
            col.append(int(char + it.__next__(), 16))

        col.append(255)

        if normalize:
            col = map(lambda x: x / 255, col)
            if precision is not None and precision > 0:
                col = map(lambda x: round(x, precision), col)

        return list(col)

    @staticmethod
    def write_stats(path, entity):
        json = ProcessHelper.read_json(path)
        print(json)
        pass

    @staticmethod
    def read_json(path):
        try:
            with open(path) as f:
                return json.loads(f.read())
        except OSError:
            print("Creation of the directory %s failed" % path)

    @staticmethod
    def write_json(file, data):
        with open(file, mode="w") as f:
            f.write(data)
