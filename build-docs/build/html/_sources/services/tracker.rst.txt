.. _Tracker Service:

Tracker Service
===============
The tracker service retrieves data communication to inform the user about data flows. It can track
the size of packets sent from every local device to which server, using which protocol over which
port.

Main thread
-----------
The main thread setups the tracker to use and stores it into the database using the Traffic model. 
Not every packet can be inserted into the database as separate packets
because the system will overflow in memory. The packets are combined in groups to limit the
number of records in the database but still store the needed details. Every minute all collected
groups from the previous minute will be uploaded to the database in bulk. Groups will be created
based on source, destination, protocol, and service. If it is not needed to store destination, protocol,
or service, the configurations can be changed in the config file. After the records are uploaded to
the database, unknown IP addresses are added to the queue to be handled by the resolver service.

.. automodule:: tracker.thread
   :members:
   :undoc-members:
   :show-inheritance:

Tracker options
---------------
There are two packages that can retrieve the packets that will be forwarded, namely using Tcpdump and Scapy. Only
packets are tracked that go from the local network, so no incoming messages from the cloud. This
is done explicitly since the tool is about sharing personal data instead of retrieving data. The
command line output will be parsed using a regex matcher, which retrieves the needed information
from the package.

Tcpdump tracker
~~~~~~~~~~~~~~~

.. automodule:: tracker.tcp_dump_tracker
   :members:
   :undoc-members:
   :show-inheritance:

Scapy tracker
~~~~~~~~~~~~~

.. automodule:: tracker.scapy_tracker
   :members:
   :undoc-members:
   :show-inheritance:




