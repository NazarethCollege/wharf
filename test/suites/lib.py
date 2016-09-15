import os

def config_path(folder, file):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs/{}/{}'.format(folder, file))