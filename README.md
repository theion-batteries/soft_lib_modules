# Module Library

####  Definition of Module: ####
In this project, a module contains two things:
    
    Hardware Module:
                    sensor, high voltage devices, CNC controller
    Software Module: 
                    Interface to connect with the Hardware module 
                    using communication protocol (eg:TCP/IP) 
                    and control the devices


The project template helps  to create a **Software Module** for the corresponding **Hardware module** 


A **Software Module** can use following communication protocol:

    o TCP/IP
    o Serial 
    o Keyence Communication over TCP/IP
    o Meteor Communication over TCP/IP

## **asyncio**:

This library heavily use the features of [**asyncio**](https://docs.python.org/3/library/asyncio.html) library from Python for TCP/IP and Serial Communication.

Refer  to official documentation to get familiar with the library and its features


## **Module** 

A **class** of the **Software Module** contains module components and individual functions to send commands and receive
data from the hardware modules.

### Module Component 
A Module component Contains 

    o Module name - unique name to identify the Hardware Module  Eg: sample_module, cnt_motion 
    o Module Type - Type of the module  Eg: SampleModule, GrblModule (Reason to give
        type: There can be two hardware module of the same type. We have cnt_motion, whs_motion
        which is of GrblModule type)
    o Network Parameters - information include ip, port, timeout, buffersize. 
    o Commands - commands for the Hardware module


These informations are configured in an YAML file and saved under **./config/** folder as given in the template


#### Example YAML file:

    module_type: GrblModule   # Type of the grbl module
    commands:                 # list of commands implemented in grbl Module  
      unlock: $X              # individual command name and corresponding actions
      reset_unlock: ""
      move: X
      move_check: X
    
    cnt_motion:              # name of the Grbl Module 
      network:               # network parameters
          ip: "192.168.0.203" 
          port: 8882
          timeout: 10
          buffer_size: 4096
    
    whs_motion:             # Another Grbl Module in house and its network params
      network:
        ip: "1921.168.0.204"
        port: 8882
        timeout: 10
        buffer_size: 4096
    


#### Settings: 
In case of Grbl module, the custom settings are defined in **YAML** 
    file stored under **./config/settings/** folder




### Building a Software Module

To create a class for a new Software Module, we have to inherit the **Module** base class


**Module** base class contains function required for any hardware modules such as

    connect
    disconnect
    sleep



A new Software Module should inherit from the Module Base class.
    
    class SampleModule(Module):
    yaml_file_name = "sample_module.yaml" # name of the yaml file containing the configuration
                                            settings for the Software Module

    def __init__(self, module_name: str):
        eol: str = "\n"
        ack_str: str = "ok" + eol
        Module.__init__(
            self,
            eol=eol,
            ack_str=ack_str,
            yaml_file=self.yaml_file_name,
            module_name=module_name)   # Initialize the Module base class with End of line identifier
                                         acknowledgement string, yaml file name and individual module 
                                         name





















