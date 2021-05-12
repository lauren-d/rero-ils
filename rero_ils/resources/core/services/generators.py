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

"""Permissions generators."""

from elasticsearch_dsl import Q
from invenio_records_permissions.generators import Generator
# TODO: use proxy for current_librarian ?
from rero_ils.modules.patrons.api import current_librarian


class OwningOrganisationPermissionMixin(Generator):
    """Allow to limit access to records of its owning organisation."""

    def query_filter(self, record=None, **kwargs):
        """Filter to apply to the query."""

        return Q(
            'term',
            metadata__organisation__pid=current_librarian.organisation_pid)
