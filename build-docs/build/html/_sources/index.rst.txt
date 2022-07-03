=======================================
Welcome to PrivateHome's documentation!
=======================================

The PrivateHome controller is a controller which will enhance your privacy inside your own home. 
It will act as a gateway between your Smart Home devices and the rest of the world. 

Purposes
========

The controller has 3 main purposes:

 ========== ================================================================== 
  Purpose    Description                                                       
 ========== ================================================================== 
  Inform     Inform who is sending a amount of data where                          
  Control    Setup your smart home system with the functionalities you want   
  Monitor    Block or allow data flows inside and outside of the network   
 ========== ================================================================== 

Inform
------
The controller tracks all outgoing data using the :ref:`Tracker Service` and :ref:`Resolver Service`. It can track the following things:

* When
* From which device
* To which server (group) 
* Size
* Location of server
* A guess for which functionality

Control
-------
Using the controller you can setup which functionalities you want to enable for each smart home device you have connected to the network. 
You are able to block specific devices or specific destinations if you do not want to send data to a or any company. 
This is done using the :ref:`Web Service`.

Monitor
-------
The controller can block specific outgoing traffic according to the things you have setup inside your dashboard. 
This is done using the :ref:`Firewall Service`.

Dashboard
=========
.. |private_home_link| raw:: html

   <a href="http://private-home.local:8888" target="_blank">http://private-home.local:8888</a>

When everything is installed we can access the dashboard through the following link |private_home_link|.
Here you can control the entire application add new discovered devices and investigate the data flows.

.. note::
   If the link does not work, you can also try it with the ip address of the local machine. If you are connected to the smart home network this will be ``192.168.2.1``.

.. toctree::
   :hidden:
   :maxdepth: 1
   :numbered:
   :caption: Home
   
   self

Repositories
============
.. toctree::
   :caption: Repositories
   
   Controller repository <https://github.com/stijnkamp/privacy-controller>
   Vue frontend repository <https://github.com/stijnkamp/private-home-interface>

Installation
=============
We separate the installation between the hardware setup and the software setup.

.. toctree::
   :maxdepth: 1
   :numbered:
   :caption: Installation
   
   installation/hardware
   installation/software

Start scripts
=============
The controller has two main scripts which you can run. One is the main controller which you can run using ``main.py``. 
The other is ``benchmark.py`` which can be used to benchmark the tracking of TCP packets. 

.. toctree::
   :maxdepth: 1
   :numbered:
   :caption: Start scripts

   start_scripts/main
   start_scripts/benchmark

Shared variables
================

.. toctree::
   :maxdepth: 1
   :numbered:
   :caption: Shared variables

   shared/config
   shared/state
   shared/utils

Services
========

.. toctree::
   :maxdepth: 5
   :numbered:
   :caption: Services
   
   services/web
   services/firewall
   services/tracker
   services/resolver
   services/websocket
