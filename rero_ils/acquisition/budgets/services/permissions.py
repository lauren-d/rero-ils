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

"""Budgets permissions."""

from invenio_records_permissions import BasePermissionPolicy

from rero_ils.resources.core.services.permissions import RolePermissionPolicy


class BudgetRecordPermissionPolicy(BasePermissionPolicy):
    """Access control configuration for budget resources."""

    # TODO :: NEED_TO_BE_FIXED
    #  (2021-05-13)
    #  At this time, the `query_filter` used to list record (using permissions
    #  `can_search`) isn't the `query_filter` declared in the corresponding
    #  permission class ; instead this is the `query_filter` method defined
    #  into the into the `can_read` that is used.
    #  This is due to the default "read" value specified by `_search` method of
    #  `invenio_records_resources.records.service.RecordService` class.

    can_search = [RolePermissionPolicy('librarian', 'system_librarian')]
    can_read = [RolePermissionPolicy('librarian', 'system_librarian')]
    can_create = [RolePermissionPolicy('system_librarian')]
    can_update = [RolePermissionPolicy('system_librarian')]
    can_delete = [RolePermissionPolicy('system_librarian')]
