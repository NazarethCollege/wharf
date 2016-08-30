import click, os
from . import settings, configuration, process_manager
import tempfile
from distutils import dir_util


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.argument('config_path')
@click.argument('command', default='dev')
def run(config_path, command='dev'):
    abs_config_path = os.path.abspath(config_path)
    config = configuration.Config.load_from(abs_config_path)
    tmp_dir = tempfile.mkdtemp(dir='/tmp')
    dir_util.copy_tree(
        os.path.join(os.path.dirname(__file__), 'docker'),
        tmp_dir
    )

    config.volumes.append('{}:/docker'.format(tmp_dir))
    process_manager.build_image(config, logger=click.echo)
    process_manager.run_image(config, command, logger=click.echo)


@cli.command()
def version():
    major, minor, patch = settings.VERSION

    click.echo("Wharf version {}.{}.{} compiled at {}".format(
        major,
        minor,
        patch,
        settings.COMPILATION_DATE.strftime('%Y-%m-%d %H:%M:%S')
    ))


