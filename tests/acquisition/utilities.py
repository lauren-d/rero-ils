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

"""Utilities for acquitition."""


from rero_ils.acquisition.proxies import current_acquisition
from rero_ils.resources.core.services.permissions import \
    system_libarian_identity


def create_acquisition_resource(resource_type, data):
    """Utility for creation of budget."""
    service = current_acquisition.get_service(resource_type)
    return service.create(system_libarian_identity, data)
