benchmark.py script
===================
The benchmark script is mainly used to check if every packet that is send through the gateway will be processed by a TCP tracker. Unfortunately bigger packets are dropped by the system. 
In the current situation the controller retrieves around 80% of all packets, depending on the load of the tracker.

.. automodule:: benchmarks.raw_send
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: benchmarks.wetransfer
   :members:
   :undoc-members:
   :show-inheritance:

