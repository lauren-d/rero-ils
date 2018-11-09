# -*- coding: utf-8 -*-
#
# This file is part of RERO ILS.
# Copyright (C) 2018 RERO.
#
# RERO ILS is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# RERO ILS is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RERO ILS; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Click command-line interface for patrons_types record management."""

from __future__ import absolute_import, print_function

import json

import click
from flask.cli import with_appcontext

from ..organisations.api import Organisation
from .api import PatronType


@click.command('importpatronstypes')
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.argument('infile', type=click.File('r'))
@with_appcontext
def import_patrons_type(infile, verbose):
    """Import patron types.

    infile: Json patrons_types file
    """
    click.secho(
        'Import patron types:',
        fg='green'
    )

    data = json.load(infile)
    for patron_type_data in data:
        if verbose:
            click.echo('\tPatron Type: ' + patron_type_data['name'])
        organisation = Organisation.get_record_by_pid(
            patron_type_data['organisation_pid']
        )
        if organisation:
            PatronType.create(patron_type_data, dbcommit=True, reindex=True)
        else:
            click.secho(
                'Organisation PID not found: {pid}'.format(
                    pid=patron_type_data['organisation_pid']
                ),
                fg='red'
            )