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

import logging
import uuid

import numpy as np
from .names.adjectives import adjectives
from .names.nouns import nouns


class BaseLogger(object):

    def __init__(self, name="", unique_id=None, logger=None):
        """
        A name should be a mnemonic string which makes it easy to derive
        the type and association of an object throughout the logs. Further
        it is not useful as a dict key since the name may not be unique.
        For unique dict keys the unique_id is the right tool to use.

        A unique id is used to identify every object uniquely without
        resorting to the id mechanism of Python (unique_id may not be changed).
        If it is None it will be generated, if it is a string this string will
        be used. This is only intended to be used to reconstruct an object
        hierarchy after loading.

        The logger is the object which is responsible for logging. If None
        a new one is created with the name of the object. If it is not None
        the one provided is used which is useful to spit out log files or logs
        in e.g. a GUI.

        The observer interface is added to the BaseLogger since maybe not only
        the optimizable classes should be coupled to observers.
        """

        self.setKind()
        self.setName(name)
        self.__unique_id = str(uuid.uuid4()).lower() if unique_id is None\
            else unique_id

        self.list_observers = []

        if logger is None:
            logger = logging.getLogger(name=self.__name)
        self.logger = logger
        # self.debug("logger \"" + name + "\" created")

    def setKind(self):
        self.kind = "baselogger"

    def setName(self, name):
        if name == "":
            my_index_ad = np.random.randint(0, len(adjectives))
            my_index_no = np.random.randint(0, len(nouns))

            my_adjective = adjectives[my_index_ad]
            my_noun = nouns[my_index_no]
            name = my_adjective + "_" + my_noun + "_" + self.kind
            # name = re.sub('-', '_', str(uuid.uuid4()).lower())
            # bring into form which can also be used by FreeCAD

        self.__name = name

    def getName(self):
        return self.__name

    name = property(fget=getName, fset=setName)

    def getUniqueId(self):
        return self.__unique_id

    unique_id = property(fget=getUniqueId, fset=None)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def getBasicInfo(self):
        return {"name": self.name,
                "unique_id": self.unique_id,
                "kind": self.kind,
                "protocol_version": 0}

    def __getstate__(self):
        """
        Deleting logger is necessary to prevent deepcopy from aborting due to
        a not pickleable thread.lock object.
        """
        state = self.__dict__.copy()
        del state["logger"]

        return state

    def __setstate__(self, state):
        """
        We have to restore the logger manually.
        """
        self.__dict__.update(state)
        self.logger = logging.getLogger(name=self.name)

    def appendObservers(self, obslist):
        self.list_observers += obslist

    def informObservers(self):
        for obs in self.list_observers:
            obs.informAboutUpdate()
