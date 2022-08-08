Usage
=====

Dependencies
************


Buzzard requires several python packages.
They may be installed with

.. code-block:: console

  pip install -r requirements.txt



Command Line Usage
******************

.. code-block:: console

  python buzzard.py <configFile> <options>

The configuration file can be either a ``.py``-file containing a dictionary called ``config`` or a ``.json``-file containing a single dictionary with the configuration.

Example configuration file (python format)
******************************************

.. literalinclude:: ../../examples/LinearElastic/config.py
   :language: python
   :caption: File: ``examples/LinearElastic/config.py``

Example configuration file (json format)
****************************************

.. literalinclude:: ../../examples/LinearElastic/config.json
   :language: json
   :caption: File: ``examples/LinearElastic/config.json``
