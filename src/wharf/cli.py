import click
from . import settings, api


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.argument('config_path')
@click.argument('command', default='dev')
def run(config_path, command='dev'):
    api.run(config_path, command, click.echo)


@cli.command()
@click.argument("config_path")
@click.argument("template")
def create_configuration(config_path, template):
    config = api.create_configuration(config_path, template)
    click.echo(config)


@cli.command()
@click.argument("config_path")
@click.option('--format', type=click.Choice(['systemd']), default='systemd')
def create_init_file(config_path, format):
    config = api.create_init_file(config_path, format)
    click.echo(config)


@cli.command()
def version():
    major, minor, patch = settings.VERSION

    click.echo("Wharf version {}.{}.{} compiled on {}".format(
        major,
        minor,
        patch,
        settings.COMPILATION_DATE.strftime('%Y-%m-%d %H:%M:%S')
    ))


