State
=====
The state is shared between all services. There are 2 main functionalities of the state class. 

* All queues between the different services
* The current dhcp leases, automatically updated when a new lease has been given. 

Queueing system
---------------
In some cases we need to send a message or command to another service. This is done with queues. From any service you can add something to the queue for another service. 
And a service can wait for a command in the queue to execute. 

.. automodule:: state
   :members:
   :undoc-members:
   :show-inheritance:
