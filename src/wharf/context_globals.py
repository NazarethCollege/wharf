import docker, dockerpty, os
from ipaddress import IPv4Network, IPv4Address
import socket
from . import api


_conns = []

def next_ip(network_name, context):
    client = docker.APIClient(version="auto")
    network = client.inspect_network(network_name)

    subnet = IPv4Network(network['IPAM']['Config'][0]['Subnet'])
    reserved = [IPv4Address(v['IPv4Address'].split('/')[0]) for k,v in network['Containers'].items()]
    
    subnet_hosts = subnet.hosts()
    next(subnet_hosts) #skip first address
    for address in subnet_hosts:
        if address in reserved: continue
        
        return str(address)

    raise Exception("Could not find unused address in subnet {}".format(subnet))


def random_open_port(context):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _conns.append(tcp)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    
    return str(port)


def load_properties(paths, context):
    if type(paths) is not list:
        paths = [paths,]
    
    file_found = False
    for path in paths:
        try:
            if context:
                properties = api.load_properties(os.path.join(os.path.dirname(context.file_location), path))
            else:
                properties = api.load_properties(path)

            file_found = True
        except FileNotFoundError:
            pass

    if not file_found:
        raise FileNotFoundError("None of the following properties files were found: {}".format(','.join(paths)))
    
    return properties


def before_container_start():
    for conn in _conns:
        conn.close()    


def global_wrap(func, context):
    def wrapper(*args, **kwargs):
        return func(*args, **{**kwargs, **{ 'context': context } })

    return wrapper


def wrap_globals(context):
    wrapped_globals = {}
    for key in globals.keys():
        wrapped_globals[key] = global_wrap(globals[key], context)

    return wrapped_globals


globals = {
    'next_ip': next_ip,
    'random_open_port': random_open_port,
    'load_properties': load_properties
}
