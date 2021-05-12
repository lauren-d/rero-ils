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

"""Budgets record resource configuration."""

from marshmallow import fields
from flask_resources import JSONDeserializer, JSONSerializer, \
    RequestBodyParser, ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.records.headers import etag_headers
from ..serializers.reference_encoder import ReferenceEncoder


class BaseRecordResourceConfig(RecordResourceConfig):
    """Budgets resource configuration."""

    # blueprint_name = 'budgets'
    url_prefix = "/records"
    routes = {
        "list": "/",
        "list-permissions": "/<pid_type>/permissions",
    }

    request_view_args = {
        "pid_type": fields.Str(),
    }

    # Response handling
    response_handlers = {
        "application/json": ResponseHandler(
            JSONSerializer(encoder=ReferenceEncoder), headers=etag_headers)
    }
