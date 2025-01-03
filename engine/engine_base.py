from abc import ABC, abstractmethod


class EngineBase(ABC):

    @abstractmethod
    def go(self):
        pass

    @abstractmethod
    def filter_details(self):
        pass

    @abstractmethod
    def get_material(self, d):
        pass

    @abstractmethod
    def process_details(self):
        pass

    @abstractmethod
    def preprocess_details(self, d):
        pass

    @abstractmethod
    def set_default(self):
        pass

    @abstractmethod
    def before_render(self, d):
        pass

    @abstractmethod
    def render_partial(self, d):
        pass

    @abstractmethod
    def set_material(self, m):
        pass

    @abstractmethod
    def save_small(self, b, s):
        pass

    @abstractmethod
    def set_scene(self):
        pass

    @abstractmethod
    def render_detail(self, result):
        pass
