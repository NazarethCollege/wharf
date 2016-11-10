Configuration
==========================================

The Wharf configuration file is processed using ``templated-yaml``, so it has some advanced features that will not be covered in this document.  Following is
a list of keys recognized and parsed by Wharf and their default values.

Keys
-------------------

-----

wharf
~~~~~~~~~~~~~~~~~~~

**min_version** - Default: ``"0.0.0"``

Wharf meta-data, such as the minimum version required to parse this config file.

.. code-block:: yaml

  wharf:
    min_version: "0.3.4"

name
~~~~~~~~~~~~~~~~~~~

Default: ``None``

The name of the image when it's running.  You can use this to stop or kill the container.  

.. code-block:: yaml

  name: wharf

dockerfile
~~~~~~~~~~~~~~~~~~~

Default: ``None``

This is the contents of your Dockerfile, and is passed into docker-py when creating your image.  Refer to Docker documentation when constructing this value.

.. code-block:: yaml

   dockerfile: |
     FROM phusion/baseimage:0.9.19

     RUN apt-get install -y \
         sudo \
         python3-venv \
         python3-pip

     ENTRYPOINT ["/docker/entrypoint"]

dockerignore
~~~~~~~~~~~~~~~~~~~

Default: ``[]``

A list of paths to ignore when passing context to the Docker daemon.

.. code-block:: yaml

  dockerignore:
    - config/
    - readme

image
~~~~~~~~~~~~~~~~~~~

The repository and tag for your image.  Wharf will automatically tag your image after building and before running it.

.. code-block:: yaml

   image:
     repository: naz/Wharf
     tag: v1

environment
~~~~~~~~~~~~~~~~~~~

Default: ``{}``

A mapping of key:value pairs used to set environment variables on container start.  The keys and values are case sensitive.

.. code-block:: yaml

   environment:
     VAR1: value1
     VAR2: value2

volumes
~~~~~~~~~~~~~~~~~~~

Default: ``None``

A list of volumes to mount when the container starts.  The syntax is passed directly to docker-py so it supports whatever version of Docker you are running.  The
volumes also support home directory expansion (~/directory) and relative paths (../directory) with respect to the location of the configuration file.

.. code-block:: yaml

   volumes:
     - ../:/workspace
     - /etc/configs:/etc/configs

port_mappings
~~~~~~~~~~~~~~~~~~~

Default: ``[]``

A list of mappings used to map ports on the host to ports on the container and provide external access to container services.  This can also use the ``random_open_port``
global helper function.

.. code-block:: yaml

  port_mappings:
    - host: "{{ random_open_port() }}"
      container: 8080
    - host: 9090
      container: 80

entrypoint
~~~~~~~~~~~~~~~~~~~

Default: ``/docker/entrypoint``

The entrypoint script used when running docker.  

.. code-block:: yaml

  entrypoint: /entrypoint.sh

hostname
~~~~~~~~~~~~~~~~~~~

Default: ``None``

The hostname of the image when it's running.  

.. code-block:: yaml

  hostname: wharf-dev

extra_hosts
~~~~~~~~~~~~~~~~~~~

Default: ``None``

A dictionary of host-to-ip mappings that are automatically added to /etc/hosts

.. code-block:: yaml

  extra_hosts:
    testhost: "10.0.0.110"

network
~~~~~~~~~~~~~~~~~~~

Default: ``wharf.configuration.NetworkConfig``

A network configuration used to hook this container up to other dev environments.  This configuration element uses the ``next_ip`` global function to 
return the next unused ip in the passed-in network.  Use alias to declare how you would like other containers to reach this container.  Use links to 
access another container by name instead of by using volatile ip addresses.

.. code-block:: yaml

  network:
    name: wharfnet
    ipv4_address: "{{ next_ip('wharfnet') }}"
    aliases:
      - "wharf.dev"
    links:
      postgres.dev: postgres
      redis.dev: redis 

Global Helpers
-------------------

-----

Helpers can be used in the YAML file by using the special handlebars syntax ``{{ helper_name(argument) }}``

next_ip(network)
~~~~~~~~~~~~~~~~~~~

Takes the name of the network as displayed by ``docker network ls`` and returns the next available ip.

random_open_port()
~~~~~~~~~~~~~~~~~~~

Finds a random open port on the host machine to bind to.

.. toctree::