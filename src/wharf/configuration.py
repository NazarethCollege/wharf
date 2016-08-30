import yaml
from collections import namedtuple


ImageConfig = namedtuple('ImageConfig', ['repository', 'tag'])


class Config(object):

    @classmethod
    def load_from(cls, path):
        config = Config()
        config._file_location = path
        with open(path, 'r') as yaml_file:
            config._data = yaml.load(yaml_file)

        return config

    @property
    def file_location(self):
        return self._file_location

    @property
    def dockerfile(self):
        return self._data.get('dockerfile')

    @property
    def image(self):
        image_data = self._data.get('image')
        return ImageConfig(image_data.get('repository'), image_data.get('tag'))

    @property
    def environment(self):
        return self._data.get('environment', {})

    @property
    def volumes(self):
        return self._data.get('volumes', {})



