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

"""Click command-line utilities."""

import json
import sys

import click
from flask.cli import with_appcontext
from invenio_db import db

from rero_ils.acquisition.proxies import current_acquisition
from rero_ils.modules.utils import read_json_record
from rero_ils.resources.core.services.permissions import \
    system_libarian_identity


@click.group()
def acquisition():
    """Acquisition management commands."""


@acquisition.command('create')
@click.option('-a', '--append', 'append', is_flag=True, default=False)
@click.option('-t', '--type', 'resource_type', default=None)
@click.option('-l', '--lazy', 'lazy', is_flag=True, default=False)
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option('-o', '--dont-stop', 'dont_stop', is_flag=True, default=False)
@click.argument('infile', type=click.File('r'), default=sys.stdin)
@with_appcontext
def create_resources(resource_type, infile, lazy, append, verbose, dont_stop):
    """Load RERO-ILS resources."""
    try:
        service = current_acquisition.get_service(resource_type)
        if service is None:
            raise Exception(f'Unable to find resource "{resource_type}"')
        records = read_json_record(infile) if lazy else json.load(infile)
        pids = []

        for idx, record_metadata in enumerate(records, 1):
            record = service.create(system_libarian_identity, record_metadata)
            if append:
                pids.append(record.id)
            if verbose:
                message = f'<{resource_type}:{record.data["id"]}> created'
                click.echo(f'{idx:<8} {message}')
        db.session.commit()

        if append:
            click.secho(f'Append fixtures new identifiers: {len(pids)}')
            identifier = service.record_cls.pid.provider
            try:
                identifier.append(
                    sorted(pids, key=lambda x: int(x)),
                )
            except Exception as err:
                click.secho(
                    f'ERROR append fixtures new identifiers: {err}',
                    fg='red'
                )
    except Exception as e:
        click.secho('ERROR :: ' + str(e), fg='red')
        if not dont_stop:
            sys.exit(1)


@acquisition.command('test_resources')
@with_appcontext
def test_resources():
    """Tests."""
    service \
        = current_acquisition.get_service('budgets')
    pid = '1'

    # =========================================================================
    # Dumper
    # =========================================================================
    # print('==========================')
    # print('Dumper')
    # print('==========================')
    # print(service.record_cls.pid)
    # record = service.record_cls.pid.resolve(pid)
    # print('resolved record:', record)
    # print('dumped record:', record.dumps())

    # =========================================================================
    # Use record class to create resource
    # =========================================================================
    # print('===================================')
    # print('Use record class to create resource')
    # print('===================================')
    # from rero_ils.acquisition.budgets.records.api import Budget
    # data = {
    #     "metadata": {
    #       "name": "2021",
    #       "start_date": "2021-01-01",
    #       "end_date": "2021-12-31",
    #       "is_active": True,
    #       "organisation": {
    #         "$ref": "https://ils.rero.ch/api/organisations/1"
    #       }
    #     }
    #   }
    # rec = Budget.create(data)
    # rec.commit()
    # db.session.commit()
    # print(rec)

    # =========================================================================
    # Use service to create resource
    # =========================================================================
    # print('==============================')
    # print('Use service to create resource')
    # print('==============================')
    # data = {
    #     "metadata": {
    #         "name": "2021",
    #         "start_date": "2021-01-01",
    #         "end_date": "2021-12-31",
    #         "is_active": True,
    #         "organisation": {
    #             "$ref": "https://ils.rero.ch/api/organisations/1"
    #         }
    #     }
    # }
    # rec = service.create(system_libarian_identity, data)
    # print(rec)

    # =========================================================================
    # Use service to reindex resource
    # =========================================================================
    # service.reindex(system_libarian_identity, id='9')
    # print(service.indexer.__dict__)
    # TODO: indexer = self._get_record_class(payload).get_indexer_class()
    #       AttributeError: 'NoneType' object has no attribute
    #       'get_indexer_class'

    # =========================================================================
    # Access to referenced field
    # =========================================================================
    # print('==========================')
    # print('Access to referenced field')
    # print('==========================')
    # record = service.read(pid, system_libarian_identity)._obj
    # print('record:', record)
    # print('organisation field   :', record.organisation)
    # # print('organisation value   :', record.organisation.value)
    # print('organisation pid     :', record.organisation.pid)
    # print('organisation record  :', record.organisation.record)

    # =========================================================================
    # Marshmallow post_dump()
    # =========================================================================
    # record = service.read(pid, system_libarian_identity)._obj
    # print('read record:', record)
    # record['metadata']['name'] = 'WAZAAAAAA'
    # record.commit()
    # db.session.commit()
    # rec = service.update(pid, system_libarian_identity, record)._obj
    #
    # # test update record
    # record['metadata']['name'] = 'TOTO'
    # service.update(pid, system_libarian_identity, record)
    # record = service.read(pid, system_libarian_identity).data
    # print('read record updated:', record)

    # record['metadata']['name'] = '2020'
    # service.update('1', system_libarian_identity, record)
    # record = service.read(pid, system_libarian_identity).data
    # print('check inital record:', record)

    # print(record['metadata']['name'])
    # record['metadata']['name'] = 'test'
    # record.commit()
    # record = service.record_cls.pid.resolve(pid)
    # print('updated record:', record)
    # record['metadata']['name'] = '2020'
    # record.commit()
    # # print('resolve original record:', record)

    # record = Budget.create({
    #     "id": "5",
    #     "metadata": {
    #       "name": "TEST",
    #       "start_date": "2020-01-01",
    #       "end_date": "2020-12-31",
    #       "is_active": True,
    #       "organisation": {
    #         "$ref": "https://ils.rero.ch/api/organisations/1"
    #       }
    #     }})
    # db.session.commit()
    # print(record)
    # # record['metadata']['name']
    # # record.update(record)
