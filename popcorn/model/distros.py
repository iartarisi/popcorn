# -*- coding: utf-8 -*-
# Copyright (c) 2011 Ionuț Arțăriși <iartarisi@suse.cz>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from popcorn.configs import rdb
from popcorn.model.utils import list_to_tuples
from popcorn.model.error import DoesNotExist

class Distro(object):
    """A Distro is a versioned distribution e.g. openSUSE 11.4, Fedora 15

    It is identified by its name and version.

    Systems belong to a distro and their ids are stored in the list
    distro:%(distro)s:%systems

    The hash distro:%(distro) holds information about a distro:
     - name - the distro name
     - version - the version of the distribution

    """
    @classmethod
    def get_all_ids(self):
        """Return a list with all the Distro ids"""
        return rdb.smembers('distros')

    @classmethod
    def find(cls, distro_id):
        """Return a Distro object by id"""
        name, version = rdb.hmget('distro:%s' % distro_id,
                                  ['name', 'version'])
        if None in (name, version):
            raise DoesNotExist("Distro", distro_id)
        obj = cls.__new__(cls)
        obj.id, obj.name, obj.version = distro_id, name, version
        obj._key = 'distro:%s-%s' % (name, version)
        return obj

    def __init__(self, name, version):
        """Create a new Distro or retrieve an already existing one"""
        self.name = name
        self.version = version
        self._key = 'distro:%s-%s' % (name, version)
        try:
            self.id = rdb[self._key]
        except KeyError:
            self.id = str(rdb.incr('global:nextDistroId'))
            rdb[self._key] = self.id
            rdb.hmset('distro:%s' % self.id, {"name":name, "version":version})
            rdb.sadd('distros', self.id)

    def add_system(self, system_id):
        """Add a System to this distribution"""
        rdb.sadd('distro:%s:systems' % self.id, system_id)

    @property
    def systems(self):
        """Return a list of all the System objects belonging to this Distro

        Returns a list of tuples of this form: (sys_hwuuid, sys_arch)

        """
        systems = rdb.sort('distro:%s:systems' % self.id,
                           by='system:*', get=['#', 'system:*->hw_uuid'])
        return list_to_tuples(systems, 2)
        
    def __repr__(self):
        return '<Distro %s>' % self.id
