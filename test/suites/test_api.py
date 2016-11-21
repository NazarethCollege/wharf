from wharf import api, configuration
from lib import *
from unittest.mock import patch
import pytest


@patch('wharf.process_manager.build_image')
@patch('wharf.process_manager.run_image')
def test_min_version_succeed(mocked_build, mocked_run):
    api.run(config_path('min-version-pass', 'input.yml'))

    assert mocked_build.called
    assert mocked_run.called


def test_min_version_fail():
    with pytest.raises(configuration.ConfigurationError):
        api.run(config_path('min-version-fail', 'input.yml'))


@patch('wharf.process_manager.build_image')
@patch('wharf.process_manager.run_image')
def test_build_with_context_exclude(mocked_build, mocked_run):
    api.run(config_path('exclude-context', 'input.yml'))
    config = mocked_build.call_args[0][0]

    assert config.dockerignore == ['first/path', '!second/path']


def test_generate_systemd():
    config = api.create_init_file(config_path('systemd', 'input.yml'), 'systemd')
    with open(config_path('systemd', 'expected-output.yml')) as handle: expected = handle.read() 

    assert config == expected