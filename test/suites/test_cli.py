import os, subprocess
from lib import *


def expected_output(config):
    path = config_path(config, 'expected-output')
    contents = ''
    with open(path, 'r') as file_handle:
        contents = file_handle.read()

    return contents


def run_command(*args):
    wharf_binary = os.environ['WHARF_EXECUTABLE']
    return subprocess.run([wharf_binary] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_version():
    version = run_command('version')
    assert version.returncode == 0
    assert os.environ['WHARF_VERSION'] in str(version.stdout)


def test_create_configuration():
    result = run_command('create_configuration', config_path('simple', 'input.yml'), config_path('simple', 'template.tpl'))
    assert str(result.stdout.decode('utf-8')) == expected_output('simple')
