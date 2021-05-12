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

"""ILSBaseRecord Service API config."""

from invenio_records_resources.services import RecordServiceConfig


from .components import PIDComponent
from .results import BaseRecordItem, BaseRecordList


class IlsBaseRecordServiceConfig(RecordServiceConfig):
    """ILS base record Service configuration."""

    result_item_cls = BaseRecordItem
    result_list_cls = BaseRecordList

    components = RecordServiceConfig.components + [
        PIDComponent,
    ]
