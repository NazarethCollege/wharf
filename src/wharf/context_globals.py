import docker, dockerpty, os
from ipaddress import IPv4Network, IPv4Address
import socket


_conns = []

def next_ip(network_name):
    client = docker.Client(version="auto")
    network = client.inspect_network(network_name)

    subnet = IPv4Network(network['IPAM']['Config'][0]['Subnet'])
    reserved = [IPv4Address(v['IPv4Address'].split('/')[0]) for k,v in network['Containers'].items()]
    
    subnet_hosts = subnet.hosts()
    next(subnet_hosts) #skip first address
    for address in subnet_hosts:
        if address in reserved: continue
        
        return str(address)

    raise Exception("Could not find unused address in subnet {}".format(subnet))


def random_open_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _conns.append(tcp)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    
    return str(port)


def before_container_start():
    for conn in _conns:
        conn.close()

globals = {
    'next_ip': next_ip,
    'random_open_port': random_open_port
}