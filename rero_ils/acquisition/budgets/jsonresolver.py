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

"""Budgets resolver."""

import jsonresolver
from flask import current_app


@jsonresolver.route('/api/budgets/<pid>', host='bib.rero.ch')
def budget_resolver(pid):
    """Resolve referenced budget."""
    record = current_app.extensions['rero-ils-acquisition'] \
        .resources['budgets'].service.record_cls.pid.resolve(pid)
    return {
        'pid': record['id'],
        'type': 'budgets'
    }
