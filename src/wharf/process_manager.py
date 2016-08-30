import docker, dockerpty, os
from io import BytesIO
import json


def build_image(config, logger=lambda x: None):
    client = docker.Client()
    encoded_dockerfile = BytesIO(config.dockerfile.encode('utf-8'))
    for output in client.build(
        fileobj=encoded_dockerfile,
        rm=True,
        tag="{}:{}".format(config.image.repository, config.image.tag)
    ):
        lines = [json.loads(l) for l in output.decode('utf-8').split('\r\n') if len(l.strip())]
        error = False
        for line in lines:
            if line.get('stream'):
                logger(line['stream'].replace('\n', ''))
            else:
                error = True
                logger(line.get('errorDetail', {}).get('message').replace('\n', ''))

    if error:
        raise Exception("Failed to build image")


def run_image(config, command, logger=lambda x: None):
    client = docker.Client()

    all_volumes = config.volumes
    volumes = [v.split(':')[1] for v in all_volumes]

    binds = []
    for volume in all_volumes:
        parts = volume.split(':')
        host_path = parts[0]
        guest_path = parts[1]

        if not os.path.isabs(host_path):
            host_path = os.path.realpath(
                os.path.join(
                    os.path.dirname(config.file_location),
                    host_path
                )
            )

        parts[0] = host_path
        binds.append(":".join(parts))

    env = {
        'LOCAL_USER_ID': os.getuid()
    }
    env.update(config.environment)

    container = client.create_container(
        image='{}:{}'.format(config.image.repository, config.image.tag),
        stdin_open=True,
        tty=True,
        command=command,
        volumes=volumes,
        host_config=client.create_host_config(binds=binds),
        environment=env
    )

    pty = dockerpty.start(client, container)