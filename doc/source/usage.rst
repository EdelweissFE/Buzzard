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

.. literalinclude:: ../../testfiles/edelweiss/LinearElastic/config.py
   :language: python
   :caption: File: ``testfiles/LinearElastic/edelweiss/config.py``

Example configuration file (json format)
****************************************

.. literalinclude:: ../../testfiles/edelweiss/LinearElasticJSON/config.json
   :language: json
   :caption: File: ``testfiles/edelweiss/LinearElasticJSON/config.json``
