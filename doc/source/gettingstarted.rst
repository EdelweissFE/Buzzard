Getting started
===============

As Buzzard is developed to best work with the finite element code |EdelweissFE|
together with the material models and finite elements provided by |Marmot|, we recommend to install the
respective libraries first. For the installation of Marmot and EdelweissFE we refer to
the steps given in |EdelweissFEinstall|.

.. |EdelweissFE| raw:: html

   <a href="https://github.com/EdelweissFE/EdelweissFE" target="_blank">EdelweissFE</a>

.. |EdelweissFEinstall| raw:: html

   <a href="https://edelweissfe.github.io/EdelweissFE/installation.html" target="_blank">EdelweissFE Installation</a>

.. |Marmot| raw:: html

   <a href="https://github.com/MAteRialMOdelingToolbox/Marmot" target="_blank">Marmot</a>

Installation
************

Buzzard depends on several packages which are summarized below.

.. literalinclude:: ../../requirements.txt

They may be installed with

.. code-block:: console

  python -m pip install -r requirements.txt

Command Line Usage
******************

.. code-block:: console

  python buzzard.py <configFile> <options>

The configuration file can be either a ``.py``-file containing a dictionary called ``config`` or a ``.json``-file containing a single dictionary with the configuration.
