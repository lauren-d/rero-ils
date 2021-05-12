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

"""Tests REST API for budget resource."""


from rero_ils.acquisition.budgets.records.api import Budget


def test_budget_api(app, budget_2020_martigny_test_data):
    """Test the REST API for a budget resource."""
    # from pprint import pprint
    # pprint(budget_2020_martigny_data)
    # pprint(budget_2020_martigny)
    # assert True
    from pprint import pprint

    print('test_budget_api:', budget_2020_martigny_test_data)
    # identity = Identity(1)
    # identity.provides.add(UserNeed(1))
    # # identity.provides.add(Need(method='system_role', value='any_user'))
    # identity.provides.add(Need(method='role', value='system_librarian'))
    #
    # service = current_acquisition.get_service('budget')
    # record = service.create(identity, budget_2020_martigny_test_data)
    record = Budget.create(budget_2020_martigny_test_data)
    pprint(record)
    assert True
