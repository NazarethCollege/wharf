.. Wharf documentation master file.

Welcome to Wharf's documentation!
==========================================

Wharf is a command-line tool used to simplify Docker development environments.  It combines build and runtime Docker configuration for one image/container in a
YAML environment file.

Wharf is primarily meant to be used as a development tool, but can also be used to produce production images in a continuous integration environment.  In the Naz environment,
Wharf is usually also installed inside a container to provide container-specific helper functions.

To contribute to the project visit https://github.com/NazarethCollege/wharf  Pull requests are welcome!

.. toctree::
   :maxdepth: 2

   installation
   usage/index
   configuration/index
   defaultentrypoint