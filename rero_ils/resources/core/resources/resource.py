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

"""Budgets record resource."""

from flask import abort, g
from flask_resources import request_parser, resource_requestctx, \
    response_handler, route
from invenio_records_resources.resources.records.resource import \
    request_data, request_search_args, request_view_args
from marshmallow_utils.fields import SanitizedUnicode

from invenio_records_resources.resources import RecordResource


class BaserRecordResource(RecordResource):
    """Budgets record resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        url_rules = super(BaserRecordResource, self).create_url_rules()
        url_rules += [
            route("GET", routes["list-permissions"], self.search_permissions),
        ]

        return url_rules

    @request_view_args
    @response_handler()
    def search_permissions(self):
        """Read permissions.

        GET /budgets/permissions
        """
        permissions = self.service.read_permissions(g.identity)
        return permissions, 200
