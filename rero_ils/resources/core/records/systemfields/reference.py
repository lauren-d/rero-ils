# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2021 RERO
# Copyright (C) 2021 UCLouvain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Generic fields for RERO-ILS resources."""

from invenio_records.systemfields.base import SystemField

from rero_ils.modules.utils import extracted_data_from_ref


class ReferenceField(SystemField):
    """Describe a reference metadata about a RERO-ILS resource.

    In many resource, you could find a `$ref` key pointing to another RERO-ILS
    project resource. This class allow to extract easily some useful data from
    this reference URI. Available attributes for this class are: 'value',
    'pid', 'type' and 'record'.

    .. code-block:: python

       class MyRecord(ilsBaseRecord):
       organisation = ReferenceField(key='metadata.organisation')

    you could access the Organisation on a record you get from the
    database:

    .. code-block:: python

        record = MyRecord.get_record()
        record.organisation.pid  # would return the PID of organisation object.
        record.organisation.type  # would return PID type of the resource.
        record.organisation.record  # would return a Organisation object.
        record.organisation.value  # would return the reference value.
    """

    # TODO: validate if reference exist into the system

    def __init__(self, key='id', dump_key=['pid', 'type']):
        """Initialize the ReferenceField."""
        self._ref = None
        self._dump_key = dump_key
        super().__init__(key=key)

    @property
    def value(self):
        """."""
        return self._ref

    @property
    def pid(self):
        """."""
        return extracted_data_from_ref(self._ref)

    @property
    def type(self):
        """."""
        return extracted_data_from_ref(self._ref, data='resource')

    @property
    def record(self):
        """."""
        return extracted_data_from_ref(self._ref, data='record')

    @property
    def dump_key(self):
        """."""
        return self._dump_key

    def obj(self, instance):
        """Get the access object."""
        obj = self._get_cache(instance)
        if obj is not None:
            return obj

        data = self.get_dictkey(instance)
        if data:
            self._ref = data
            obj = self
        self._set_cache(instance, obj)
        return obj

    def dump(self):
        """Dump the reference link."""
        return {
            'pid': self.pid,
            'type': self.type,
        }

    def __get__(self, record, owner=None):
        """Get the record's access object."""
        if record is None:
            # access by class
            return self

        # access by object
        return self.obj(record)

    #
    # Record extension
    #
    # def pre_commit(self, record):
    #     """Initialise the model field."""
    #     # TODO: may we can validate reference here ?
