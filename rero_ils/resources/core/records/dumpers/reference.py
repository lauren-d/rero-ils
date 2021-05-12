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

"""Elasticsearch dumpers for organisation information."""

from invenio_records.dictutils import dict_set
from invenio_records.dumpers import ElasticsearchDumperExt

from ..systemfields.reference import ReferenceField


class ReferenceDumperExt(ElasticsearchDumperExt):
    """Dumper for all reference from RERO-ILS resources."""

    @staticmethod
    def _iter_referencefields(record_cls):
        """Internal helper method to extract all reference fields."""
        for attr_name in dir(record_cls):
            systemfield = getattr(record_cls, attr_name)
            if isinstance(systemfield, ReferenceField):
                if systemfield.dump:
                    yield systemfield

    def dump(self, record, dump_data):
        """Dump the references recursively.

        The method replace each reference by a dictionary containing the
        following keys (if the record has a ReferenceField defined):
        - ``pid`` - Pid of the resource.
        - ``type`` - PID type of the resource.
        """
        # Dump all reference fields defined as system fields.
        for systemfield in self._iter_referencefields(record.__class__):
            dict_set(
                dump_data,
                systemfield.key,
                systemfield.obj(record).dump()
            )
        return dump_data
