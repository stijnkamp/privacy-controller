.. _Firewall Service:

Firewall Service
================
A firewall is needed in order to  intercept packages that are needed/wanted inside your local smart home setup.

NF-tables
---------
This service is updating a kernel running program named `NF-tables <https://wiki.nftables.org/wiki-nftables/index.php/Main_Page>`_, which is the standard that is already installed on most Linux devices.
It is the new version of ip-tables, but is has the same approach. 

General flow
------------
This service takes all devices from the database and setup rules for the firewall to drop packets that are on the blacklist.
When all rules are configured it will set those rules inside the kernels program, which will then be updated to apply with these new rules. 
Next it is waiting for a queue command to check again the devices and setup the rules. 


Classes and functions
---------------------

.. automodule:: firewall
   :members:
   :undoc-members:
   :show-inheritance:


Firewall commands
~~~~~~~~~~~~~~~~~
This class contains all the commands that can be done by putting them inside the Firewall queue

.. automodule:: firewall.firewall_commands
   :members:
   :undoc-members:
   :show-inheritance:

RuleParser
~~~~~~~~~~
This class is used to create the nf-tables rules from the known devices inside the database.

.. automodule:: firewall.rule_parser
   :members:
   :undoc-members:
   :show-inheritance:


