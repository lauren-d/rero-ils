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

"""RERO-ILS resources base class."""

from flask_resources import request_parser
from invenio_pidstore.models import PIDStatus
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import PIDStatusCheckField
from marshmallow_utils.fields import SanitizedUnicode


request_pids_args = request_parser(
    {"client": SanitizedUnicode()}, location='args'
)


class IlsBaseRecord(Record):
    """Base class for any RERO-ILS resources.

    WARNING: extensions must be defined in each child classes.
    see : https://github.com/inveniosoftware/invenio-records/blob/master/
          invenio_records/extensions.py#L73
    """
    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED)

    def reindex(self):
        """Reindex the record."""
        # TODO :: implement this method.

