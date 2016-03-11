#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
brical.py
=====

This module contains the class `LanguageInterpreter` which interprets 
the contents of BriCA language files.

"""

# BriCA Language Interpreter for V1 (Interpreter version 0)
#  Originally licenced for WBAI (wbai.jp) under the Apache License (?)
#  Created: 2015-07-18

# TODO: import, subports

import sys
import numpy
import brica1
import json

from components.motor_area_component import MotorAreaComponent
from components.hippocampus_component import HippocampusComponent
from components.visual_area_component import VisualAreaComponent

class LanguageInterpreter:
    """
    The BriCA language interpreter.
    - reads BriCA language files.
    - creates a BriCA agent based on the file contents.
    """
    __unit_dic={}	# Map: BriCA unit name ⇒ unit object
    __jsn = None	# json object for a BriCA graph
    __super_modules={}	# Super modules
    base_name_space=""	# Base Name Space

    def __init__(self):
        """ Create a new `LanguageInterpreter` instance.

        Args:
          None.

        Returns:
          LanguageInterpreter: a new `LanguageInterpreter` instance.

        """
        __unit_dic={}
        __super_modules={}

    def load_file(self, file_object):
        """ Load a BriCA language json file.

        Args:
          A file object

        Returns:
          A module dictionary: {module name, unit instance} pairs

        """
	self.__jsn = json.load(file_object)
	if not "Header" in self.__jsn:
	    print >> sys.stderr, "Header must be specified!"
	    return
	header = self.__jsn["Header"]
	if not "Base" in header:
	    print >> sys.stderr, "Base name space must be specified!"
	    return
	if "Type" in header:
	    self.__type=header["Type"]
	self.base_name_space = header["Base"].strip()
	self.__add_modules()
	self.__add_ports()
	self.__add_connections()
	return self.__unit_dic

    def create_agent(self, scheduler):
        """ Add top level modules to a BriCA agent (to be called after load_file).

        Args:
          A brica1.Scheduler object

        Returns:
          A BriCA agent

        """
	# Checking grounding
	sub_modules = self.__sub_modules()
	for unit_key in self.__unit_dic:
	    if not unit_key in sub_modules:
		try:
		    module = self.__unit_dic[unit_key]
		    component = module.get_component(unit_key)
		    # TODO: Setting aliases here according to the current spec.
		    for port in module.in_ports:
			length=module.get_in_port(port).buffer.shape[0]
			component.make_in_port(port, length)
			component.alias_in_port(module, port, port)
		    for port in module.out_ports:
			length=module.get_out_port(port).buffer.shape[0]
			component.make_out_port(port, length)
			component.alias_out_port(module, port, port)
		except KeyError:
		    print >> sys.stderr, "Module " + unit_key + " at the bottom not grounded as a Component!"
		    return
	# Checking undefined modules
	for unit_key in self.__super_modules:
	    if not unit_key in self.__unit_dic:
		print >> sys.stderr, "SuperModule " + unit_key + " not defined!"
	for unit_key in sub_modules:
	    if not unit_key in self.__unit_dic:
		print >> sys.stderr, "SuperModule " + unit_key + " not defined!"
	# Main logic
	top_module = brica1.Module()
	for unit_key in self.__unit_dic.keys():
	    if not unit_key in self.__super_modules:
		if isinstance(self.__unit_dic[unit_key], brica1.Module):
		    top_module.add_submodule(unit_key, self.__unit_dic[unit_key])
		    print "Adding a module " + unit_key + " to a BriCA agent."
	agent = brica1.Agent(scheduler)
	agent.add_submodule("__Runtime_Top_Module", top_module)
	return agent

    def __sub_modules(self):
	sub_modules = {}
	for unit in self.__unit_dic:
	    if unit in self.__super_modules:
		sub_modules[self.__super_modules[unit]] = unit
	return sub_modules

    def __add_modules(self):
        """ Add modules from the JSON description
        Args:
          None
        Returns:
          None
        """
	if "Modules" in self.__jsn:
	    modules = self.__jsn["Modules"]
	    for module in modules:
		self.__add_a_module(module)
	else:
	    print >> sys.stderr, "Warning: No `Modules` in the language file."

    def __add_a_module(self, module):
	module_name = module["Name"].strip()
	if module_name == "":
	    return
	module_name = self.__prefix_base_name_space(module_name)		# Prefixing the base name space
	if not module_name in self.__unit_dic:
	    print "Creating " + module_name + "."
	    self.__unit_dic[module_name]=brica1.Module()	# New Module instance
	    if module_name in self.__super_modules and self.__super_modules[module_name] in self.__unit_dic:
		# Registering it as a submodule according to previously defined hierarchy.
		self.__unit_dic[self.__super_modules[module_name]].add_submodule(self.__unit_dic[module_name])
	    for submodule in self.__super_modules:
		# Registering it as a supermodule according to previously defined hierarchy.
		if self.__super_modules[submodule]==module_name and submodule in self.__unit_dic:
		    self.__unit_dic[module_name].add_submodule(self.__unit_dic[submodule])
	if "ImplClass" in module:
	    # if an implementation class is specified
	    implclass = module["ImplClass"].strip()
	    if implclass != "":
		print "Use the existing ImplClass " + implclass + " for " + module_name + "."
		try:
		    component = eval(implclass+'()')	# New ImplClass instance
		    self.__unit_dic[module_name].add_component(module_name, component)
		except:
		    print >> sys.stderr, "Component " + implclass + " not found for " +  module_name + "!"
	if "SuperModule" in module:
	    supermodule=module["SuperModule"].strip()
	    if supermodule != "":
		supermodule = self.__prefix_base_name_space(supermodule)
		self.__add_subunit(supermodule,module_name)
	if "SubModules" in module:
	    for submodule in module["SubModules"]:
		submodule = self.__prefix_base_name_space(submodule)
		self.__add_subunit(module_name,submodule) 

    def __prefix_base_name_space(self, name):
	if name.find(".")<0:
	    return self.base_name_space + "." + name
	else:
	    return name

    def __add_subunit(self, superunit, subunit):
	if subunit in self.__super_modules:
	    print >> sys.stderr, "Cannot add SubModule " + subunit + " twice!"
	    return
	if self.__loop_check(superunit, subunit):
	    print >> sys.stderr, "Loop detected while trying to add " + subunit + " as a subunit to " + superunit + "!"
	    return
	self.__super_modules[subunit] = superunit
	if not subunit in self.__unit_dic:
	    print >> sys.stderr, "SubModule " + subunit + "has not been defined."
	    return
	if not superunit in self.__unit_dic:
	    print >> sys.stderr, "SuperModule " + superunit + "has not been defined."
	    return
	if isinstance(self.__unit_dic[subunit], brica1.Module):
	    self.__unit_dic[superunit].add_submodule(subunit, self.__unit_dic[subunit])
	    print "Adding a module " + subunit + " to " + superunit + "."

    def __loop_check(self, superunit, subunit):
	if superunit == subunit:
	   return True
	val = superunit
	while val in self.__super_modules:
	    val = self.__super_modules[val]
	    if val == subunit:
		return True
	return False

    def __add_ports(self):
        """ Add ports from the JSON description

        Args:
          None

        Returns:
          None

        """
	if "Ports" in self.__jsn:
	    ports = self.__jsn["Ports"]
	    for port in ports:
		self.__add_a_port(port)
	else:
	    print >> sys.stderr, "Warning: No `Ports` in the language file."

    def __add_a_port(self, port):
	try:
	    port_module = port["Module"].strip()	# TODO: "Unit"?
	    port_module = self.__prefix_base_name_space(port_module)
	except KeyError:
	    print >> sys.stderr, "Module not specified while adding a port!"
	    return
	try:
	    port_type = port["Type"].strip()
	except KeyError:
	    print >> sys.stderr, "Type not specified while adding a port!"
	    return
	try:
	    port_name = port["Name"].strip()
	except KeyError:
	    print >> sys.stderr, "Name not specified while adding a port!"
	    return
	try:
	    dimension = port["Shape"]
	except KeyError:
	    print >> sys.stderr, "Shape not specified while adding a port!"
	    return
	try:
	    length = 1
	    for i in dimension:
		length=length*i
	    if length < 1:
		print >> sys.stderr, "Port dimension < 1!"
		return
	    # Checking if the module exists
	    if port_module in self.__unit_dic:
		module=self.__unit_dic[port_module]
		if port_type == "Input":
		    try:
			# Checking if the port has been defined
			module.get_in_port(port_name)
		    except KeyError:
			module.make_in_port(port_name, length)
			print "Creating an input port " + port_name + " (length " + str(length) + ") to " + port_module + "."
		elif port_type == "Output":
		    try:
			# Checking if the port has been defined
			module.get_out_port(port_name)
		    except KeyError:
			module.make_out_port(port_name, length)
			print "Creating an output port " + port_name + " (length " + str(length) + ") to " + port_module + "."
		else:
		    print >> sys.stderr, "Invalid port type!"
	    else:
		print >> sys.stderr, "Module " + port_module + " not found!"
	except ValueError:
	    print >> sys.stderr, "Shape error for the port " + port_name + "!"
	except:
	    print >> sys.stderr, "Error creating a port " + port_name + " with the length " + str(length) + " to " + port_module + "."

    def __add_connections(self):
        """ Add connections from the JSON description

        Args:
          None

        Returns:
          None

        """
	if "Connections" in self.__jsn:
	    connections = self.__jsn["Connections"]
	    for connection in connections:
		self.__add_a_connection(connection)
	else:
	    if self.__type!="C":
		print >> sys.stderr, "Warning: No `Connections` in the language file."

    def __add_a_connection(self, connection):
	# TODO: Port length check
	try:
	    connection_name = connection["Name"]
	except KeyError:
	    print >> sys.stderr, "Name not specified while adding a connection!"
	    return
	try:
	    from_unit = connection["FromModule"]
	    from_unit = self.__prefix_base_name_space(from_unit)
	except KeyError:
	    print >> sys.stderr, "FromModule not specified while adding a connection!"
	    return
	try:
	    from_port = connection["FromPort"]
	except KeyError:
	    print >> sys.stderr, "FromPort not specified while adding a connection!"
	    return
	try:
	    to_unit = connection["ToModule"]
	    to_unit = self.__prefix_base_name_space(to_unit)
	except KeyError:
	    print >> sys.stderr, "ToModule not specified while adding a connection!"
	    return
	try:
	    to_port = connection["ToPort"]
	except KeyError:
	    print >> sys.stderr, "ToPort not specified while adding a connection!"
	    return
	# Checking if the modules have been defined.
	if not from_unit in self.__unit_dic:
	    print >> sys.stderr, "Module " + from_unit + " not defined!"
	    return
	if not to_unit in self.__unit_dic:
	    print >> sys.stderr, "Module " + to_unit + " not defined!"
	    return
	# if from_unit & to_unit belong to the same level
	if ((not from_unit in self.__super_modules) and (not to_unit in self.__super_modules)) or \
	(from_unit in self.__super_modules and to_unit in self.__super_modules and (self.__super_modules[from_unit] == self.__super_modules[to_unit])):
	    try:
		fr_port_obj = self.__unit_dic[from_unit].get_out_port(from_port)
		to_port_obj = self.__unit_dic[to_unit].get_in_port(to_port)
		if fr_port_obj.buffer.shape != to_port_obj.buffer.shape:
		    print >> sys.stderr, "Port dimension unmatch!"
		    raise Error
		# Creating a connection
		brica1.connect((self.__unit_dic[from_unit],from_port), (self.__unit_dic[to_unit],to_port))
		print "Creating a connection from " + from_port + " of " + from_unit + " to " + to_port + " of " + to_unit + "."
	    except Error:
		print >> sys.stderr, "Error adding a connection from " + from_unit + " to " + to_unit + " on the same level but not from an output port to an input port!"
		return
	# else if from_unit is the direct super module of the to_unit
	elif to_unit in self.__super_modules and self.__super_modules[to_unit]==from_unit:
	    try:
		fr_port_obj = self.__unit_dic[from_unit].get_in_port(from_port)
		to_port_obj = self.__unit_dic[to_unit].get_in_port(to_port)
		if fr_port_obj.buffer.shape != to_port_obj.buffer.shape:
		    print >> sys.stderr, "Port dimension unmatch!"
		    raise Error
		# Creating a connection (alias)
		self.__unit_dic[to_unit].alias_in_port(self.__unit_dic[from_unit], from_port, to_port)
		print "Creating a connection (alias) from " + from_port + " of " + from_unit + " to " + to_port + " of " + to_unit + "."
	    except Error:
		print >> sys.stderr, "Error adding a connection from the super module " + from_unit + " to " + to_unit + " but not from an input port to an input port!"
		return
	# else if to_unit is the direct super module of the from_unit
	elif from_unit in self.__super_modules and self.__super_modules[from_unit]==to_unit:
	    try:
		fr_port_obj = self.__unit_dic[from_unit].get_out_port(from_port)
		to_port_obj = self.__unit_dic[to_unit].get_out_port(to_port)
		if fr_port_obj.buffer.shape != to_port_obj.buffer.shape:
		    print >> sys.stderr, "Port dimension unmatch!"
		    raise Error
		# Creating a connection (alias)
		self.__unit_dic[from_unit].alias_out_port(self.__unit_dic[to_unit], to_port, from_port)
		print "Creating a connection (alias) from " + from_port + " of " + from_unit + " to " + to_port + " of " + to_unit + "."
	    except KeyError:
		print >> sys.stderr, "Error adding a connection from " + from_unit + " to its super module " + to_unit + " but not from an output port to an output port!"
		return
	# else connection level error!
	else:
	    print >> sys.stderr, "Trying to add a connection between units " + from_unit + " and " + to_unit + " in a remote level!"
	    return

print "BriCAL.py loaded!"
