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

from rero_ils.resources.core.resources import BaseRecordResourceConfig


class BudgetRecordResourceConfig(BaseRecordResourceConfig):
    """Budgets resource configuration."""

    blueprint_name = 'budgets'
    url_prefix = "/budgets"
    routes = {
        "list": "/",  # legacy to be compatible with RERO-ILS records.
        "item": "/<pid_value>",
        "item-permissions": "/<pid_value>/permissions",
    }

    request_view_args = {
        "pid_value": fields.Str(),
        "pid_type": fields.Str(),
    }
