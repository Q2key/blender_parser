from engine.saver.catalog_saver import CatalogSaver
from engine.saver.constructor_saver import ConstructorSaver


class SaverBuilder:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    def get_saver(self, builder_type):
        if builder_type == 'preset':
            return CatalogSaver(self.ctx, self.args)
        else:
            return ConstructorSaver(self.ctx, self.args)
