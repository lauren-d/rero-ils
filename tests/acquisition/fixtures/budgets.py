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

"""Budgets fixtures."""

from copy import deepcopy

import pytest
from acquisition.utilities import create_acquisition_resource


# MARTIGNY (org1) fixtures ----------------------------------------------------
@pytest.fixture(scope="module")
def budget_2020_martigny_test_data(acquisition_data):
    """Load budget data."""
    return deepcopy(acquisition_data.get('budg1'))


@pytest.fixture(scope="module")
def budget_2020_martigny(app, org_martigny, budget_2020_martigny_test_data):
    """Load budget record."""
    return create_acquisition_resource(
        'budgets', budget_2020_martigny_test_data
    )


@pytest.fixture(scope="module")
def budget_2019_martigny_data(acquisition_data):
    """Load budget data."""
    return deepcopy(acquisition_data.get('budg3'))


@pytest.fixture(scope="module")
def budget_2019_martigny(app, org_martigny, budget_2019_martigny_data):
    """Load budget record."""
    return create_acquisition_resource(
        'budgets', budget_2019_martigny_data
    )


# SION (org2) fixtures --------------------------------------------------------
@pytest.fixture(scope="module")
def budget_2020_sion_data(acquisition_data):
    """Load budget data."""
    return deepcopy(acquisition_data.get('budg2'))


@pytest.fixture(scope="module")
def budget_2020_sion(app, org_martigny, budget_2020_sion_data):
    """Load budget record."""
    return create_acquisition_resource(
        'budgets', budget_2020_sion_data
    )


# Legacy fixtures -------------------------------------------------------------

# @pytest.fixture(scope="function")
# def budget_2020_martigny_data_tmp(acquisition):
#     """Load standard budget 2020 of martigny."""
#     return deepcopy(acquisition.get('budg1'))
#
#
# @pytest.fixture(scope="module")
# def budget_2020_sion_data(acquisition):
#     """Load budget 2020 sion."""
#     return deepcopy(acquisition.get('budg2'))
#
#
# @pytest.fixture(scope="module")
# def budget_2020_martigny_data(acquisition):
#     """Load budget 2020 martigny."""
#     return deepcopy(acquisition.get('budg1'))
#
#
# @pytest.fixture(scope="module")
# def budget_2019_martigny_data(acquisition):
#     """Load budget 2019 martigny."""
#     return deepcopy(acquisition.get('budg3'))
#
#
# @pytest.fixture(scope="module")
# def budget_2018_martigny_data(acquisition):
#     """Load budget 2018 martigny."""
#     return deepcopy(acquisition.get('budg4'))
#
#
# @pytest.fixture(scope="module")
# def budget_2017_martigny_data(acquisition):
#     """Load budget 2017 martigny."""
#     return deepcopy(acquisition.get('budg5'))
#
#
# @pytest.fixture(scope="module")
# def budget_2017_martigny(
#         app, org_martigny, budget_2017_martigny_data):
#     """Load budget 2017 martigny record."""
#     budget = Budget.create(
#         data=budget_2017_martigny_data,
#         delete_pid=False,
#         dbcommit=True,
#         reindex=True)
#     return budget
#
#
# @pytest.fixture(scope="module")
# def budget_2018_martigny(
#         app, org_martigny, budget_2018_martigny_data):
#     """Load budget 2018 martigny record."""
#     budget = Budget.create(
#         data=budget_2018_martigny_data,
#         delete_pid=False,
#         dbcommit=True,
#         reindex=True)
#     return budget
#
#
# @pytest.fixture(scope="module")
# def budget_2020_martigny(
#         app, org_martigny, budget_2020_martigny_data):
#     """Load budget 2020 martigny record."""
#     budget = Budget.create(
#         data=budget_2020_martigny_data,
#         delete_pid=False,
#         dbcommit=True,
#         reindex=True)
#     return budget
#
#
# @pytest.fixture(scope="module")
# def budget_2019_martigny(
#         app, org_martigny, budget_2019_martigny_data):
#     """Load budget 2019 martigny record."""
#     budget = Budget.create(
#         data=budget_2019_martigny_data,
#         delete_pid=False,
#         dbcommit=True,
#         reindex=True)
#     return budget
#
#
# @pytest.fixture(scope="module")
# def budget_2020_sion(
#         app, org_sion, budget_2020_sion_data):
#     """Load budget 2020 sion record."""
#     budget = Budget.create(
#         data=budget_2020_sion_data,
#         delete_pid=False,
#         dbcommit=True,
#         reindex=True)
#     return budget
