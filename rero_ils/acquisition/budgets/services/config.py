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

"""Config file for Budget resource."""

from flask_babelex import gettext as _
from invenio_records_resources.services import SearchOptions
from invenio_records_resources.services.records.components import \
    MetadataComponent
from invenio_records_resources.services.records.links import RecordLink, \
    pagination_links


from rero_ils.resources.core.services.config import IlsBaseRecordServiceConfig

from rero_ils.acquisition.budgets.records.api import Budget
from rero_ils.acquisition.budgets.services.permissions import \
    BudgetRecordPermissionPolicy
from rero_ils.acquisition.budgets.services.schemas import RecordSchema


class BudgetSearchOptions(SearchOptions):
    """Mock module search options."""

    sort_default = 'bestmatch'
    sort_default_no_query = 'name'
    sort_options = {**SearchOptions.sort_options, **{
        'lastupdated': dict(
            title=_('Last updated'),
            fields=['-updated'],
        ),
        'name': dict(
            title=_('Budget name'),
            fields=['name'],
        ),
    }}


class BudgetServiceConfig(IlsBaseRecordServiceConfig):
    """Budget service configuration.

    Needs both configs, with File overwritting the record ones.
    """
    record_cls = Budget
    schema = RecordSchema

    permission_action_prefix = ""
    permission_policy_cls = BudgetRecordPermissionPolicy

    search = SearchOptions

    links_item = {
        "self": RecordLink("{+api}/budgets/{id}")
    }

    links_search = pagination_links("{+api}/budgets{?args*}")

    # indexer_cls = BudgetIndexer
