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

"""Budgets marshmallow schemas."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode

from rero_ils.resources.core.services.schemas import ReferenceSchema


class BudgetMetadataSchema(Schema):
    """Budget metadata schema class."""

    name = SanitizedUnicode(required=True)
    start_date = fields.Str(required=True)
    end_date = fields.Str(required=True)
    is_active = fields.Boolean(default=False)
    organisation = fields.Nested(ReferenceSchema, required=True)


class RecordSchema(BaseRecordSchema):
    """Budget RecordSchema class."""

    metadata = fields.Nested(BudgetMetadataSchema)
