Software installation
=====================
When we have setup the hardware in the previous section, we can install the required software packages. 

Operating System
----------------
The system should work with most of the linux operating systems. But the system is tested with Raspberry Pi OS Lite installed using the `Raspberry Pi Imager <https://www.raspberrypi.com/software/>`_.
Following the instruction inside the Raspberry Pi Imager and formatting the SD card with `Raspberry Pi OS Lite`.
After you have formatted the SD card you can insert it into the Raspberry Pi and boot up.

SSH access
----------
The installation can be done entirely inside the CLI. First we need to login into the Raspberry Pi. 
If you are connected to the same wifi, you can access the raspberry pi using the following commands:

.. code-block:: bash

   ssh pi@raspberry.local
   #enter the password: raspberry

Installing packages
-------------------
The following packages need to be installed:

 ========== ========================================= 
  Package    Purpose                                  
 ========== ========================================= 
  PiHole     Handles the DNS server and DHCP server   
  PM2        Handles to run the script on startup     
 ========== ========================================= 

To install them we first need to clone the source code and then install the packages using the ``install.sh`` script.

.. code-block:: bash

   git clone https://github.com/stijnkamp/privacy-controller private-home
   cd private-home
   chmod +x install.sh
   sudo bash install.sh

Starting the application
------------------------
To start the controller you need to follow the instructions inside :ref:`Main Script`.