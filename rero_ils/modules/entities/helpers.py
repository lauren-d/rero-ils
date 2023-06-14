# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019-2023 RERO
# Copyright (C) 2019-2023 UCLouvain
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

"""Helpers for entities."""


def str_builder(field_values, prefix='', suffix='', delimiter=''):
    """String builder method.

    :param field_values: could be a ``str`` or an array of ``str``.
    :param prefix: a ``str`` to add before field_values.
    :param suffix: a ``str`` to add after field_values.
    :param delimiter: a ``str`` used to concatenate multiple field_values.
    :return: a concatenated ``str`` or an empty string.
    """
    if not isinstance(field_values, list):
        field_values = [field_values]
    if any(field_values):
        return f'{prefix}{delimiter.join(field_values)}{suffix}'
    return ''
