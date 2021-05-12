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

"""Persistent identifier field."""

from invenio_records_resources.records.systemfields.pid import \
    PIDFieldContext as BasePIDFieldContext


class PIDFieldContext(BasePIDFieldContext):
    """PIDField context for pid.

    This class implements the class-level methods available on a PIDField
    for records.
    """

    @property
    def provider(self):
        """."""
        return self.field._provider or None

    def create(self, record):
        """Proxy to the field's create method."""
        return self.field.create(record)

    def delete(self, record):
        """Proxy to the field's delete method."""
        return self.field.delete(record)


# class PIDField(BasePIDField):
#     """Persistent identifier system field."""
#
#     def create(self, record):
#         """Method to create a new persistent identifier for the record."""
#         # This uses the fields __get__() data descriptor method below
#
#         pid = getattr(record, self.attr_name)
#         if pid is None:
#             # Create a PID if the object doesn't already have one.
#             pid = self._provider.create(
#                 object_type=self._object_type,
#                 object_uuid=record.id,
#                 record=record,
#             ).pid
#
#             # Set using the __set__() method
#             setattr(record, self.attr_name, pid)
#         return pid
