.. _Web Service:

Web Service
===========
The web service is responsible for all REST API calls to the web server, hosting the static frontend
interface, and connecting with the database. It is a Model View Controller architecture
(MVC) with different models, views, and controllers, each with its responsibilities. 

Web server
----------
webserver.py is starts up the Flask server and connect to the database. It also inserts the existing modules. 


.. automodule:: web.web_server
   :members:
   :exclude-members: catch_all, docs, docs_redirect
   :show-inheritance:

Database
--------
The database is a sqlite scheme. The structure is displayed in :ref:`db_structure`.

.. _db_structure:

.. figure:: ../_static/img/private_home_db.png

   Database structure

Helpers
-------
A couple of helpers are defined to help within multiple parts of the web service. 

.. automodule:: web.helpers
   :members:
   :undoc-members:
   :show-inheritance:

Modules
-------
The web service is divided into 3 modules, which each contain models and/or controllers: Api module, Auth module and Pihole module. 

API module
~~~~~~~~~~~
The api modules is the main module of the webserver which serves all endpoints except the authentication endpoint. 
The controllers are divided into 3 submodules and is represented by a Flask classfull view. 
**Devices controller**

.. automodule:: web.api.controllers.devices
   :members:
   :undoc-members: 
   :show-inheritance:

**Traffic controller**

.. automodule:: web.api.controllers.traffic
   :members:
   :undoc-members:
   :show-inheritance:

**Server group controller**

.. automodule:: web.api.controllers.server_group
   :members:
   :undoc-members:
   :show-inheritance:

Auth module
~~~~~~~~~~~
To protect all routes a auth modules is developed. The models include a user, which is stored in the database and contains the name, email and password. 
It contains a controller to fetch a token using an email address and password. It also has a decorator to check if the token send with the request is valid.

**Token controller**

.. automodule:: web.auth.controllers
   :members:
   :undoc-members:
   :show-inheritance:

**Decorator**

.. automodule:: web.auth.helpers
   :members:
   :exclude-members: optional_arg_decorator
   :show-inheritance:


Pihole module
~~~~~~~~~~~~~
The pihole module is created to make the bridge between pihole and the PrivateHome tool. This is done by connecting the Pihole database to the flask server. 
And define the needed Pihole models in this module. It includes the pihole devices discovered by the network and the including network addresses. 
