Usage
==========================================

Wharf exposes as much of the `docker-py <https://github.com/docker/docker-py>`_ API as is currently useful.  We have no need or plan for 100%
support and add features as needed.

Create configuration
-------

.. code-block:: bash

  wharf create_configuration CONFIG_PATH TEMPLATE

Performs variable substitution on a template found at TEMPLATE using a YAML config file found at CONFIG_PATH.  Variable substitution is performed using the
``templated-yaml`` library, which supports Jinja syntax.

Run
-------

.. code-block:: bash

   wharf run [OPTIONS] CONFIG_PATH [COMMAND]
     --config-override    A YAML-formatted string that overrides values in the main configuration

Executes the configuration found at CONFIG_PATH.  If COMMAND is empty, the command "dev" is passed to the container, which is parsed
by the default entrypoint at `/docker/entrypoint`.

Version
-------

.. code-block:: bash

   wharf version

Prints the version and compile time of the package. 


.. toctree::
   :maxdepth: 2

   

