import templated_yaml.api as tapi
from collections import namedtuple


ImageConfig = namedtuple('ImageConfig', ['repository', 'tag'])
NetworkConfig = namedtuple('NetworkConfig', ['name', 'ipv4_address', 'aliases', 'links'])
PortMapping = namedtuple('PortMapping', ['host', 'container'])

class Config(object):

    @classmethod
    def load_from(cls, path):
        config = Config()
        config._file_location = path
        config._data = tapi.render_from_path(path)

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

    @property
    def port_mappings(self):
        mappings = self._data.get('port_mappings', [])
        parsed_mappings = []
        for mapping in mappings:
            parsed_mappings.append(
                PortMapping(mapping.get('host'), mapping.get('container'))
            )

        return parsed_mappings

    @property
    def entrypoint(self):
        return self._data.get('entrypoint', None)

    @property
    def hostname(self):
        return self._data.get('hostname', None)

    @property
    def name(self):
        return self._data.get('name', None)

    @property
    def extra_hosts(self):
        return self._data.get('extra_hosts', None)

    @property
    def network(self):
        network = self._data.get('network', None)
        network_config = None

        if network:
            network_config = NetworkConfig(
                network['name'],
                network['ipv4_address'],
                network.get('aliases', []),
                network.get('links', [])
            )

        return network_config


