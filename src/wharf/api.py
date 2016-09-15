from . import configuration, process_manager, api
import tempfile, jinja2
from distutils import dir_util
import os, yaml


def run(config_path, command='dev', logger=lambda x: None):
    abs_config_path = os.path.abspath(config_path)
    config = configuration.Config.load_from(abs_config_path)
    tmp_dir = tempfile.mkdtemp(dir='/tmp')
    dir_util.copy_tree(
        os.path.join(os.path.dirname(__file__), 'docker'),
        tmp_dir
    )

    config.volumes.append('{}:/docker'.format(tmp_dir))

    process_manager.build_image(config, logger)
    process_manager.run_image(config, command, logger)


def create_configuration(config_path, template_path):
    abs_config_path = os.path.abspath(config_path)
    abs_template_path = os.path.abspath(template_path)

    with open(abs_config_path, 'r') as yaml_file:
        context = yaml.load(yaml_file)

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(abs_template_path)))
    template = jinja_env.get_template(os.path.basename(abs_template_path))

    return template.render(context)