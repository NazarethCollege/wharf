import os, subprocess


def config_path(name):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs/{}/config.yml'.format(name))


def run_command(*args):
    wharf_binary = os.environ['WHARF_EXECUTABLE']
    return subprocess.run([wharf_binary] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_version():
    version = run_command('version')
    assert version.returncode == 0
    assert os.environ['WHARF_VERSION'] in str(version.stdout)


def test_run():
    result = run_command('run', config_path('simple'))
    print(result.stdout)
    print(result.stderr)