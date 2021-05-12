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

"""Service results."""

from invenio_records_resources.services.records.results import RecordItem, \
    RecordList


class BaseRecordItem(RecordItem):
    """Single record result."""

    @property
    def permissions(self):
        """Record permissions.

        Placing this functionality here because it is a projection of the
        record item's characteristics and allows us to re-use the
        underlying data layer record.
        For performance reasons, it is not embedded in the `to_dict`
        method.
        """
        record_permissions = {
            f"{action}": {'can': self._service.check_permission(
                self._identity, action, record=self._record
            )}
            for action in ['read', 'update', 'delete']
        }
        reasons = self._record.reasons_not_to_delete()
        # reasons = self._record.reasons_to_keep()
        record_permissions['delete']['can'] = \
            not reasons and record_permissions['delete']['can']
        if not record_permissions['delete']['can'] and not reasons:
            # in this case, it's because check permission return
            # `False`, so the reason is 'Permission denied'
            reasons = {'others': {'permission': 'permission denied'}}
        record_permissions['delete']['reasons'] = reasons

        return record_permissions


class BaseRecordList(RecordList):
    """List of records result."""

    @property
    def permissions(self):
        """Record permissions."""
        return {
            'list': {'can': self._service.check_permission(
                self._identity, 'search')},
            'create': {'can': self._service.check_permission(
                self._identity, 'create')},
        }

    def to_dict(self):
        """Return result as a dictionary."""
        results = super().to_dict()
        results['permissions'] = self.permissions
        return results
