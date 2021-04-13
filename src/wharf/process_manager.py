import docker, dockerpty, os
from io import BytesIO
import json
import wharf.context_globals


def build_image(config, logger=lambda x: None):
    client = docker.APIClient(version="auto")
    encoded_dockerfile = BytesIO(config.dockerfile.encode('utf-8'))

    context = docker.utils.tar(os.path.dirname(config.file_location), exclude=config.dockerignore)
    context.seek(0)

    import tarfile
    context_tar = tarfile.open(mode='a', fileobj=context)
    dfinfo = tarfile.TarInfo('Dockerfile')
    dfinfo.size = len(encoded_dockerfile.getvalue())
    context_tar.addfile(dfinfo, encoded_dockerfile)
    context_tar.close()
    context.seek(0)

    for output in client.build(
        fileobj=context,
        custom_context=True,
        rm=True,
        tag="{}:{}".format(config.image.repository, config.image.tag)
    ):
        # Bug with how the output is returned:  several dicts may be returned at once and they
        # can't be decoded until you split them.
        lines = [json.loads(l) for l in output.decode('utf-8').split('\r\n') if len(l.strip())]
        error = False
        for line in lines:
            if line.get('stream'):
                logger(line['stream'].replace('\n', ''))
            elif line.get('status'):
                logger(line['status'].replace('\n', ''))
            else:
                if 'errorDetail' in line:
                    error = True
                    logger(line.get('errorDetail', {}).get('message', '').replace('\n', ''))

    if error:
        raise Exception("Failed to build image")


def run_image(config, command, logger=lambda x: None):
    client = docker.APIClient(version="auto")

    all_volumes = config.volumes
    volumes = [v.split(':')[1] for v in all_volumes]

    binds = []
    for volume in all_volumes:
        parts = volume.split(':')
        host_path = parts[0]

        if not os.path.isabs(host_path):
            host_path = os.path.realpath(
                os.path.join(
                    os.path.dirname(config.file_location),
                    os.path.expanduser(host_path)
                )
            )

        parts[0] = host_path
        binds.append(":".join(parts))

    env = {
        'LOCAL_USER_ID': os.getuid()
    }
    env.update(config.environment)

    port_bindings = { }
    for mapping in config.port_mappings:
        port_bindings[mapping.container] = mapping.host

    if config.name:
        try:
            client.remove_container(config.name, force=True)
        except docker.errors.NotFound:
            pass

    networking_config = None
    if config.network:
        networking_config = client.create_networking_config({
            config.network.name: client.create_endpoint_config(
                ipv4_address=config.network.ipv4_address,
                aliases=config.network.aliases,
                links=config.network.links
            )
        })


    container = client.create_container(
        image='{}:{}'.format(config.image.repository, config.image.tag),
        stdin_open=True,
        tty=True,
        command=command,
        volumes=volumes,
        host_config=client.create_host_config(
            binds=binds,
            port_bindings=port_bindings,
            extra_hosts=config.extra_hosts
        ),
        environment=env,
        entrypoint=config.entrypoint,
        name=config.name,
        hostname=config.hostname,
        networking_config=networking_config
    )

    wharf.context_globals.before_container_start()
    pty = dockerpty.start(client, container)
    exit_code = int(client.inspect_container(container).get('State', {}).get('ExitCode', 0))

    return exit_code
