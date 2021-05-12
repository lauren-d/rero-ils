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

"""Permissions about RERO-ILS resources."""

from flask_principal import Identity, RoleNeed

from .generators import OwningOrganisationPermissionMixin

#
# Need instances
#
system_librarian = RoleNeed("system_librarian")
"""System librarian role for processes."""
librarian = RoleNeed("librarian")
"""Librarian role for processes."""

#
# Identities
#
system_libarian_user_id = "sys_librarian"
"""The user ID of the system librarian, used in its Identity."""
libarian_user_id = "librarian"
"""The user ID of the librarian, used in its Identity."""

system_libarian_identity = Identity(system_libarian_user_id)
"""Identity used by system librarian processes."""

libarian_identity = Identity(libarian_user_id)
"""Identity used by librarian processes."""

system_libarian_identity.provides.add(system_librarian)
libarian_identity.provides.add(librarian)


class RolePermissionPolicy(OwningOrganisationPermissionMixin):
    """Permission to limit record management by roles.

    This permission class allow any user with some roles to access and manage
    records, but only for record of its own organisation.
    NOTE : 'superuser' is always an accepted role ; not need to specify
    """

    def __init__(self, *args):
        """Permission initialization."""
        self.roles = args

    def needs(self, **kwargs):
        """Enabling needs."""
        return [RoleNeed(role) for role in self.roles]
