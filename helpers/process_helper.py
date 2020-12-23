import datetime
import os
import json

from PIL import Image


class ProcessHelper:

    @staticmethod
    def get_folder_name(root, args):
        dt = datetime.datetime.now()
        if args.version is not None:
            pt = root + "/" + args.version
        else:
            pt = root + "/" + dt.strftime("%d_%b_%Y")
        return pt

    @staticmethod
    def get_image_name(root, subfold, file, res):
        s = 's'
        b = 'b'
        l = 'l'
        return {
            "s": str.format("{0}/{1}/{2}_{3}.png", root, subfold, file, s),
            "b": str.format("{0}/{1}/{2}_{3}.png", root, subfold, file, b),
            "l": str.format("{0}/{1}/{2}_{3}.png", root, subfold, file, l),
        }

    @staticmethod
    def get_catalog_image(root, subfold, model, postifx):
        return {
            "b": str.format("{0}/{1}/{2}-{3}.png", root, subfold, model, postifx),
            "s": str.format("{0}/{1}/{2}-{3}.png", root, subfold, model, postifx)
        }

    @staticmethod
    def make_folder_by_detail(path):
        if not os.path.exists(path):
            os.makedirs(path)

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
        data_path = str.format("{0}/.dat", path)
        json_data = ProcessHelper.read_json(data_path)
        json_data[entity] = 'ok'
        ProcessHelper.write_json(data_path, json_data)

    @staticmethod
    def check_entity(path, entity):
        data_path = str.format("{0}/.dat", path)
        json_data = ProcessHelper.read_json(data_path)
        if entity in json_data:
            return False
        else:
            return True

    @staticmethod
    def read_dat_file(path):
        return ProcessHelper.read_json(str.format("{0}/.dat", path))

    @staticmethod
    def read_json(path):
        try:
            if os.path.exists(path) == False:
                ProcessHelper.write_json(path, dict(), False)

            with open(path, mode='r') as f:
                data = f.read()
                return json.loads(data)

        except OSError:
            print("Creation of the directory %s failed" % path)

    @staticmethod
    def write_json(file, data, close=True):
        with open(file, mode="w+") as f:
            f.write(json.dumps(data, indent=4))
            if close:
                f.close()
