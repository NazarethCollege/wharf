from . import configuration, process_manager, api
import tempfile, jinja2
from distutils import dir_util
import os, yaml, ast, sys, jinja2, time
from .properties import Properties
from .context_globals import wrap_globals
import templated_yaml.api as tapi


def run(config_path, command='dev', config_override=None, logger=lambda x: None):
    abs_config_path = os.path.abspath(config_path)
    override_data = tapi.render_from_string(config_override) if config_override else {}
    config = configuration.Config.load_from(abs_config_path, override_data)

    tmp_dir = tempfile.mkdtemp(dir='/tmp')
    dir_util.copy_tree(
        os.path.join(os.path.dirname(__file__), 'docker'),
        tmp_dir
    )

    config.volumes.append('{}:/docker'.format(tmp_dir))

    process_manager.build_image(config, logger)
    return process_manager.run_image(config, command, logger)


def create_configuration(config_path, template_path):
    abs_config_path = os.path.abspath(config_path)
    abs_template_path = os.path.abspath(template_path)

    context = tapi.render_from_path(abs_config_path, globals=wrap_globals(None))

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(abs_template_path)))
    template = jinja_env.get_template(os.path.basename(abs_template_path))

    return template.render(context)


def load_properties(file_location):
    p = Properties()
    p.load(open(file_location))

    return p.getPropertyDict()


def create_init_file(config_path, format):
    abs_config_path = os.path.abspath(config_path)
    config = configuration.Config.load_from(abs_config_path)

    here = os.path.dirname(os.path.abspath(__file__))

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(here, 'templates')))
    template = jinja_env.get_template('{}.j2'.format(format))
    
    return template.render({
        'wharf_file_location': abs_config_path,
        'image_name': config.name
    })