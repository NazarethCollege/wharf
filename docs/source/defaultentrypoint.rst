Default Entrypoint
==========================================

Wharf will use the following default entrypoint located at /docker/entrypoint if entrypoint is not set in the configuration document.  

.. literalinclude:: ../../src/wharf/docker/entrypoint
   :language: bash 

This entrypoint is not secure for production environments.  It creates a new user named developer with the UID of the user who runs wharf in the host.  The developer
user is able to sudo without a password and will share the host user's ~/.ssh directory if that directory has been mapped using the volumes key.

Calling ``wharf run PATH`` will create a developer user automatically.  If you want to execute something in the context of developer but do not want
to open an interactive shell you can use the following syntax.

.. code-block:: bash
  
  wharf run PATH "dev echo 'running this as developer'"

If you want to run as root and skip creating a developer, you can omit "dev" from the command.

.. code-block:: bash
  
  wharf run PATH "echo 'running this as root'"

This is not recommended except for testing, you should create a separate entrypoint specific to your application.

.. toctree::
   :maxdepth: 2

   

