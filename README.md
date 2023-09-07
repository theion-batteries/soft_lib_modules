# **Module Library**

#### *** Definition of Module:*** ####
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
Contains 

    o Module name - unique name to identify the Hardware Module  Eg: sample_module, cnt_motion 
    o Module Type - Type of the module  Eg: SampleModule, GrblModule (Reason to give
        type: There can be two hardware module of the same type. We have cnt_motion, whs_motion
        which is of GrblModule type)
    o Network Parameters - information include ip, port, timeout, buffersize. 
    o Commands - commands for the Hardware module


These informations are described in an YAML file and saved under **./config/** folder as given in the template

#### Settings: 
In case of Grbl module, the custom settings are defined in **YAML** 
    file stored under **./config/settings/** folder




### Building module component and Module 

To create a class for a new Software Module, we have to inherit the **Module** base class


**Module** base class contains function required for any hardware modules such as

    connect
    disconnect
    sleep



A Software Module should be constructed with [Module Component](#module-component) object which can constructed using 

    build_module_component(yaml_name:str, module_name: str) 
    
    o yaml_name - denotes the name of the YAML file which contains information about
                  building blocks for SoftwareModule
    o module_name - name of the associated Hardware Module.

    
The example implementation is given in **main.py** and **Sampe_Module.py**

    Step1: Create a Software Module class for its corresponding Hardware Module

    Step2: Build the components required for the Hardware and create the object for the Software Module

















