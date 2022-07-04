.. _Resolver Service:

Resolver Service
================
The primary responsibility of the resolver service is to investigate specific IP addresses. To which
device do they belong in the local network, or to which server group does it belong in the cloud
network. It retrieves information about server locations, domain names, and companies behind
the domain names.


Resolvers
---------

.. automodule:: resolver.dns_lookup
   :members:
   :undoc-members:
   :show-inheritance:


Queue commands
--------------
The resolver service waits till there is a command in the queue. There are multiple commands posisble inside the resolver service listed below. 

.. automodule:: resolver.resolver_commands
   :members:
   :undoc-members:
   :show-inheritance: