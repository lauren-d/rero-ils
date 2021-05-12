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

"""Reference encoder for serializers."""

import json
from flask import request
from rero_ils.modules.utils import extracted_data_from_ref


class ReferenceEncoder(json.JSONEncoder):
    """Reference JSONEncoder class to process reference."""

    def encode(self, o):
        """Return a JSON string representation of a Python data structure."""
        if request and request.args.get('resolve'):
            # We need to resolve `$ref`
            self._resolve_refs(o)
        return super().encode(o)

    def _resolve_refs(self, record):
        """Recursively replace the $refs.
        Replace in place all $ref to a dict of pid, type values.
        :param record: the record metadata.
        """
        for k, v in record.items():
            if isinstance(v, dict):
                if v.get('$ref'):
                    _type = extracted_data_from_ref(v, data='resource')
                    if _type:
                        resolved = dict(
                            pid=extracted_data_from_ref(v),
                            type=_type
                        )
                        record[k] = resolved
                else:
                    self._resolve_refs(v)
