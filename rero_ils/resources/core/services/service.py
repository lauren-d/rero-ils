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

"""RERO-ILS resources base service class."""

from invenio_access.permissions import system_identity
from invenio_records_resources.services.records import RecordService


class IlsBaseRecordService(RecordService):
    """RERO-ILS resources base service class."""

    def create(self, identity, data):
        """Create a record.

        :param identity: Identity of user creating the record.
        :param data: Input data according to the data schema.
        """
        # TODO: is it really needed ?
        if not identity:
            identity = system_identity
        return super().create(identity, data)

    def get_record(self, id_, identity, action='read'):
        """Get the associated record."""
        record = self.record_cls.pid.resolve(id_)
        self.require_permission(identity, action, record=record)
        return record

    def permissions(self, identity, record=None):
        """Read permissions.

        :param identity: Identity of user.
        :param record: Records instance.
        """
        permissions = {
            'list': {'can': self.check_permission(identity, 'search')},
            'create': {'can': self.check_permission(identity, 'create')}
        }
        if record:
            record_permissions = record.permissions
            permissions.update(record_permissions)

        return permissions

    def read_permission_policy(self):
        """Read a permission policy instance."""
        return self.config.permission_policy_cls
