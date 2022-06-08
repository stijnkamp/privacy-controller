.. _Main Script:


main.py script
==============
The main script is managing all sup threads. It shares the state class with those threads, and closes the threads when the program exits. 

Running the script
------------------
We need to have root permissions to access certain functionalities like the firewall settings. To run the script you can use following cmd:

.. code-block:: bash

   sudo python main.py

Run on boot
~~~~~~~~~~~
To monitor the running script and to make sure it start at boot-up we use `pm2 <https://pm2.keymetrics.io/>`_.
To install and use PM2 you can run the following commands in the root folder of the project. 

.. code-block:: bash

   # setup pm2 to start running on boot
   sudo pm2 startup
   # start the main script inside the pm2 monitor
   sudo pm2 start main.py
   # save to start the main also on boot up
   sudo pm2 save

Classes and functions
---------------------

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:



