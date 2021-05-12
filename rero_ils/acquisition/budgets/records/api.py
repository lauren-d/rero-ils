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

"""Budgets API."""

from invenio_records.dumpers import ElasticsearchDumper
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField, PIDField

from rero_ils.modules.proxies import current_ils
from rero_ils.resources.core.records import IlsBaseRecord
from rero_ils.resources.core.records.dumpers import ReferenceDumperExt
from rero_ils.resources.core.records.systemfields import PIDFieldContext, \
    ReferenceField
from rero_ils.resources.core.services.providers import ResourceIdProvider

from rero_ils.acquisition.budgets.records import models


class BudgetRecordIdProvider(ResourceIdProvider):
    """Budget PID provider."""

    identifier = models.BudgetRecordIdentifier
    pid_type = 'budget'


class Budget(IlsBaseRecord):
    """API for budget resources."""

    # Configuration
    model_cls = models.BudgetRecordMetadata
    # PID type retrieved from provider
    pid_type = BudgetRecordIdProvider.pid_type

    # Schema fields
    # TODO : retrieve base_url from config
    schema_path = 'https://ils.rero.ch/schemas/budgets/budget-v0.0.1.json'
    schema = ConstantField('$schema', schema_path)

    # System fields
    index = IndexField('budgets-budget-v0.0.1', search_alias='budgets')

    pid = PIDField(
        'id',
        provider=BudgetRecordIdProvider,
        context_cls=PIDFieldContext,
        create=False
    )

    organisation = ReferenceField('metadata.organisation')

    # Dumper
    dumper = ElasticsearchDumper(
        extensions=[ReferenceDumperExt()]
    )

    def get_number_of_acq_accounts(self):
        """Get number of acq accounts."""
        results = current_ils.acq_account_search_cls.filter(
            'term', budget__pid=self.pid.pid_value).source().count()
        return results

    def get_links_to_me(self):
        """Get number of links."""
        links = {}
        acq_accounts = self.get_number_of_acq_accounts()
        if acq_accounts:
            links['acq_accounts'] = acq_accounts
        return links

    def reasons_not_to_delete(self):
        """Get reasons not to delete record."""
        cannot_delete = {}
        others = self.reasons_to_keep()
        if others:
            cannot_delete['others'] = others
        links = self.get_links_to_me()
        if links:
            cannot_delete['links'] = links
        return cannot_delete

    def reasons_to_keep(self):
        """Reasons aside from record_links to keep a budget."""
        others = {}
        organisation = self.organisation.record

        if organisation.get('current_budget_pid') == self.pid.pid_value:
            others['is_default'] = True
        return others
