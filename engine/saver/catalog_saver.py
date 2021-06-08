from engine.saver.base_saver import BaseSaver
from engine.saver.pillow_provider import PillowProvider


class CatalogSaver(BaseSaver):

    def process(self):
        ns = self.get_name_spaces()
        src = self.ctx.SCENE["TempFile"]

        out_s = ns['s']
        out_b = ns['b']
        out_xs = ns['xs']

        res_s = self.ctx.SCENE['Resolution']['Small']
        res_b = self.ctx.SCENE['Resolution']['Big']
        res_xs = self.ctx.SCENE['Resolution']['XSmall']

        PillowProvider.save_as_jpg(src, out_s, res_s)
        PillowProvider.save_as_jpg(src, out_b, res_b)
        PillowProvider.save_as_jpg(src, out_xs, res_xs)

    def get_name_spaces(self):
        raw_str = self.parts[0]
        i = 0
        while i < len(self.parts):
            part = self.parts[i]
            if i > 0:
                raw_str = raw_str + "/" + part
            i += 1

        return {
            "xs": str.format("{0}_{1}.jpg", raw_str, 'xs').lower(),
            "s": str.format("{0}_{1}.jpg", raw_str, 's').lower(),
            "b": str.format("{0}_{1}.jpg", raw_str, 'b').lower()
        }

    def set_paths_hierarchy(self, parts):
        self.parts = parts
