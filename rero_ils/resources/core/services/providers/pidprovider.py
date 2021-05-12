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

"""Ressource ID provider."""

from invenio_db import db
from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider


class ResourceIdProvider(BaseProvider):
    """Resource identifier provider."""

    identifier = None

    pid_type = None
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.
    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of ids.
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, record=None, **kwargs):
        """Create a new persistent identifier."""
        assert record is not None, "Missing or invalid 'record'."
        kwargs.setdefault('pid_value', record.get('id'))
        if not kwargs['pid_value']:
            kwargs['pid_value'] = str(cls.identifier.next())

        try:
            if cls.get(kwargs['pid_value'], cls.pid_type):
                raise PIDAlreadyExists(
                    cls.pid_type,
                    kwargs['pid_value'],
                    'PIDAlreadyExists'
                )
        except PIDDoesNotExistError:
            kwargs.setdefault('status', cls.default_status)
            if object_type and object_uuid:
                kwargs['status'] = PIDStatus.REGISTERED
            return super().create(
                object_type=object_type, object_uuid=object_uuid, **kwargs
            )

    @classmethod
    def append(cls, pids, limit=100000):
        """Append pids into identifier table and update its sequence."""
        for idx, pid in enumerate(pids, 1):
            db.session.add(cls.identifier(recid=pid))
            if idx % limit == 0:
                db.session.commit()
        db.session.commit()
        cls.identifier._set_sequence(cls.identifier.max())
