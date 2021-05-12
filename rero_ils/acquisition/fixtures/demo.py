# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019 RERO
# Copyright (C) 2020 UCLouvain
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

"""Fake demo budgets."""

import json


def fake_budgets():
    """Create budgets for demo purposes."""
    data = {
        "metadata": {
            "name": "2020",
            "start_date": "2020-01-01",
            "end_date": "2020-12-31",
            "is_active": False,
            "organisation": {
                "$ref": "https://ils.rero.ch/api/organisations/1"
            }
        }
    }
    return json.loads(json.dumps(data))
