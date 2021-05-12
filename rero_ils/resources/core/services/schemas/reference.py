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

"""Shared Marshmallow schemas for the RERO-ILS project."""

from marshmallow import Schema, fields  # , post_dump, post_load, pre_dump

from rero_ils.modules.utils import extracted_data_from_ref


class ReferenceSchema(Schema):
    """Schema to describe a reference.

    Into many of the JSON schema, we use a `$ref` key pointing to an other
    resource from RERO-ILS. This class allow to describe this reference and
    allow to use it easily : Some data are extracted from the `$ref` as
    properties of this class :

      * pid: the pid of the referenced object.
      * type: the resource type of the referenced object.
      * record: the resource corresponding to the reference as an object.
    """

    class Meta:
        """Meta class."""

        fields = ['$ref', 'pid', 'type']

    ref = fields.URL(data_key='$ref', required=True)

    # @post_dump
    def process_reference(self, data, **kwargs):
        """Process reference."""
        data['pid'] = extracted_data_from_ref(data['$ref'])
        data['type'] = extracted_data_from_ref(data['$ref'], data='resource')
        return data
