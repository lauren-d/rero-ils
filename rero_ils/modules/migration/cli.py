# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019-2022 RERO
# Copyright (C) 2019-2022 UCLouvain
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

"""Click command-line utilities."""

from __future__ import absolute_import, print_function

import click
from flask.cli import with_appcontext
from invenio_db import db
from sqlalchemy import func

from rero_ils.modules.utils import get_record_class_from_schema_or_pid_type, \
    get_ref_for_pid


@click.group()
def migrate():
    """Migration management commands."""


@migrate.command('merge_organisation')
@click.argument('source_org_pid')
@click.argument('dest_org_pid')
@click.option('-f', '--force', is_flag=True, default=False)
@with_appcontext
def merge_organisation(source_org_pid, dest_org_pid, force):
    """Merge organisation."""

    resources_with_org = [
        'vndr'
    ]

    def _update_organisation_in_database(self, record_cls, old_org_ref,
                                         new_org_ref):
        """."""
        count = record_cls.model_cls.query\
            .filter(record_cls.model_cls.json['organisation']['$ref']
                    .as_string() == old_org_ref)\
            .update(
                {
                   "json": func.jsonb_set(
                       record_cls.model_cls.json,
                       '{organisation,$ref}',
                       f'"{new_org_ref}"')
                }, synchronize_session=False)

        db.session.commit()
        print(f"{count} update {record_cls.__class__}")

    old_org_ref = get_ref_for_pid('org', source_org_pid)
    new_org_ref = get_ref_for_pid('org', dest_org_pid)
    for pid_type in resources_with_org:
        record_cls = get_record_class_from_schema_or_pid_type(pid_type)
        _update_organisation_in_database(record_cls, old_org_ref, new_org_ref)
