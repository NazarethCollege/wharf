import click, os
from . import settings, configuration, process_manager
import tempfile, jinja2
from distutils import dir_util
import yaml


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
@click.argument("config_path")
@click.argument("template")
def create_configuration(config_path, template):
    abs_config_path = os.path.abspath(config_path)
    abs_template_path = os.path.abspath(template)

    with open(abs_config_path, 'r') as yaml_file:
        context = yaml.load(yaml_file)

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(abs_template_path)))
    template = jinja_env.get_template(os.path.basename(abs_template_path))

    click.echo(template.render(context))


@cli.command()
def version():
    major, minor, patch = settings.VERSION

    click.echo("Wharf version {}.{}.{} compiled on {}".format(
        major,
        minor,
        patch,
        settings.COMPILATION_DATE.strftime('%Y-%m-%d %H:%M:%S')
    ))


