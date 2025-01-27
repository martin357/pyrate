#!/usr/bin/env/python
"""
Pyrate - Optical raytracing based on Python

Copyright (C) 2014-2018
               by     Moritz Esslinger moritz.esslinger@web.de
               and    Johannes Hartung j.hartung@gmx.net
               and    Uwe Lippmann  uwe.lippmann@web.de
               and    Thomas Heinze t.heinze@uni-jena.de
               and    others

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from .Interface_Identifiers import *
from .Interface_Helpers import *


import uuid

from .Object_Material import MaterialObject

# TODO: material catalogue can either be filled by reading yaml files from
# refractive-index.info or by reading a complete data base
# subgroups are given by shelfs, books, ...
# different material data bases are possible
# objects are interfaces for isotropic, grin, anisotropic, catalogue, etc.

class MaterialCatalogueObject:


    def __init__(self, doc, name):
        self.__doc = doc # e.g. ActiveDocument
        self.__group = doc.addObject("App::DocumentObjectGroup", name + "_" + uuidToName(uuid.uuid4())) # materials catalogue group
        self.__group.Label = name

        self.__obj = doc.addObject("App::FeaturePython", name + Object_MaterialCatalogue_Properties_Label)
        self.__group.addObject(self.__obj)
        self.__obj.addProperty("App::PropertyStringList", "comment", "Comment", "comment lines").comment = []
        self.__obj.addProperty("App::PropertyString", "NameMaterialsCatalogue", "Comment", "name of material catalogue").NameMaterialsCatalogue = self.__group.Name

        self.__obj.setEditorMode("NameMaterialsCatalogue", 1) # readonly


        self.__obj.Proxy = self
        # TODO: load/save

    def addMaterial(self, mattype, name, **kwargs):
        MaterialObject(self.__doc, self.__group, name, mattype, **kwargs)


