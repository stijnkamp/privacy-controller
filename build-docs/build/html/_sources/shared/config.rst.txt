Configuration
=============
The application has some configurations you could change in the config folder. 

* All configurations for the Flask web server are inside the flask variable. 
* All configurations for the websocket server are inside the websocket variable

Smart Home Services
-------------------
For each Smart Home alliance we configure which services they provide and what can be configured by the user itself. 

configuration.json
~~~~~~~~~~~~~~~~~~
Each Smart Home alliance has a separate folder inside the ``services`` folder. 
That folder has a ``configuration.json`` which stores all the information needed to use the new service inside the application.

The structure of the configuration file is as follows:

**Alliance**
The organization that has build one or multiple devices or online services.

 ================= =============== ========================================================================
  Fields            Type            Description                                                                       
 ================= =============== ========================================================================
  slug              str             A unique slug which identifies the alliance                                       
  device_types[]    DeviceType[]    An array with device types that the alliance offers                               
  server_groups[]   ServerGroup[]   An array of known server groups                      
  data_types[]      DataType[]      An array of extra data types which are not in the general configuration                                                  
 ================= =============== ========================================================================

**DeviceType**
A smart home device that can be installed in your local network.

 ==================== ========================== ===================================================
  Fields               Type                       Description                                 
 ==================== ========================== =================================================== 
  slug                 str                        A unique slug which represents the device   
  name                 str                        A readable name for the device              
  icon                 str                        A relative path in the assets folder to icon image
  functionalities[]    DeviceFunctionality[]      An array of all functionalities provided    
 ==================== ========================== ===================================================

**DeviceFunctionality**
A specific functionality of a smart home device which you could enable or disable. 

 ============= =========== ======================================================================================
  Fields        Type        Description                                                                         
 ============= =========== ======================================================================================
  name          str         A readable name for the functionality                                               
  services[]    Service[]   An array of service slugs i.e. {alliance_slug}.{server_group_slug}.{service_slug}   
 ============= =========== ======================================================================================

**Service**
A online or on a other local smart home device needed service in order to implement a functionality.

 =========================== ========= =========================================================================== 
  Fields                      Type      Description                                                                
 =========================== ========= =========================================================================== 
  slug                        str       A slug which describes what the service is doing                    
  device_type (optional)      str       A regex expression which says which local device can handle the service.   
  server_group  (optional)    str       A regex expression which says which server_groups can handle the service.  
  data[]                      Data[]    The data that will be send to the handling device                          
 =========================== ========= =========================================================================== 

**Data**
The data needed by a service.

 ====================== =========== ==================================================================== 
  Fields                 Type        Description                                                         
 ====================== =========== ==================================================================== 
  type                   str         A slug of the data type that is needed i.e. general.device_status   
  trigger                str         When the data will be send to the service handler                   
  storage  (optional)    str         For how long the data will be stored at the service handler         
 ====================== =========== ==================================================================== 

**DataType**
A specific data type, which is not inside the general configurations. 

 ========= ======= =================================================================================================================================================== 
  Fields    Type    Description                                                                                                     
 ========= ======= =================================================================================================================================================== 
  slug      str     A unique slug that represents the data type  
  name      str     A description of the data type                                                                                  
  icon      str     An icon which represents the data type. Can be a relative path to the assets folder or name from `Line Awesome <https://icons8.com/line-awesome>`_  
 ========= ======= =================================================================================================================================================== 

**ServerGroup**
A server group is a set of servers that can handle specific services.

 ============ ===================== ==================================================================== 
  Fields       Type                  Description                                                         
 ============ ===================== ==================================================================== 
  slug         str                   A unique slug which identifies the server group                     
  name         str                   A readable name for the server group                                
  queries[]    ServerGroupQuery[]    A array with server queries to link servers to this server group.   
 ============ ===================== ==================================================================== 

**ServerGroupQuery**
A query which makes it possible to link incoming packages to a specific server group. 

 ==================== ======= ================================================================================== 
  Fields               Type    Description                                                                       
 ==================== ======= ================================================================================== 
  domain (optional)    str     A regex expression which says which domains belongs to this server group          
  ip (optional)        str     A regex expression which says which ip addresses belongs to this server group     
  company (optional)   str     A regex expression which says which companies belongs to this server group        
 ==================== ======= ================================================================================== 


An example configuration.json file:

.. code-block:: json
   
   {
      "slug": "tuya",
      "device_types": [
         {
            "slug": "light",
            "name": "A Tuya light",
            "functionalities": [
            {
               "name": "Control using the dedicated app",
               "services": [
                  {
                  "slug": "send_cloud_commands",
                  "server_group": "tuya_servers",
                  "data": [
                     {
                        "type": "general.device_data",
                        "trigger": "Every 10 seconds"
                     }
                  ]
                  }
               ]
            }
            ]
         }
      ],
      "server_groups": [
         {
            "slug": "tuya_servers",
            "name": "Tuya servers",
            "queries": [
            {
               "domain": ".*tuya.*"
            },
            {
               "company": ".*tuya.*"
            }
            ]
         }
      ]
   }

Functions
---------

.. automodule:: config
   :members:
   :undoc-members:
   :show-inheritance:
