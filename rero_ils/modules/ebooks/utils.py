# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019 RERO
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

"""Utilities."""

from flask import current_app
from invenio_db import db
from invenio_oaiharvester.models import OAIHarvestConfig

from ..documents.api import Document
from ..holdings.api import Holding, create_holding, \
    get_holding_pid_by_doc_location_item_type
from ..organisations.api import Organisation


def add_oai_source(name, baseurl, metadataprefix='marc21',
                   setspecs='', comment='', update=False):
    """Add OAIHarvestConfig."""
    with current_app.app_context():
        source = OAIHarvestConfig.query.filter_by(name=name).first()
        if not source:
            source = OAIHarvestConfig(
                name=name,
                baseurl=baseurl,
                metadataprefix=metadataprefix,
                setspecs=setspecs,
                comment=comment
            )
            source.save()
            db.session.commit()
            return 'Added'
        elif update:
            source.name = name
            source.baseurl = baseurl
            source.metadataprefix = metadataprefix
            if setspecs != '':
                source.setspecs = setspecs
            if comment != '':
                source.comment = comment
            db.session.commit()
            return 'Updated'
        return 'Not Updated'


# def get_harvested_sources(record):
#     """Get the harvested sources from electronicLocator."""
#     harvested_sources = []
#     new_providers = []
#
#     providers = record.get('providers', [])
#     for provider in providers:
#         organisation =
#
#
#     electronic_locators = record.get('electronicLocator', [])
#     for electronic_locator in electronic_locators:
#         source = electronic_locator.get('source')
#         if source:
#             harvested_sources.append({
#                 'source': source,
#                 'uri': electronic_locator.get('url')
#             })
#         else:
#             new_electronic_locators.append(electronic_locator)
#     if new_electronic_locators:
#         record['electronicLocator'] = new_electronic_locators
#     return harvested_sources


def create_document_holding(record):
    """Create a document and a holding for a harvested ebook."""
    # harvested_sources = get_harvested_sources(record)
    new_record = None
    doc_created = False
    providers = record.get('providers', [])
    uri = record.get(
        'electronicLocator')[0].get('url')
    for provider in providers:
        org = Organisation.get_record_by_pid(provider['organisation'])
        if org:
            if not doc_created:
                new_record = Document.create(
                    record,
                    dbcommit=True,
                    reindex=True
                )
            if new_record:
                doc_created = True
                item_type_pid = org.online_circulation_category()
                locations = org.get_online_locations()
                electronic_location = {
                    'source': '{provider} - {collection}'.format(
                        provider=provider['provider'],
                        collection=provider['collection']),
                    'uri': uri
                }
                for location_pid in locations:

                    create_holding(
                        document_pid=new_record.pid,
                        location_pid=location_pid,
                        item_type_pid=item_type_pid,
                        electronic_location=electronic_location,
                        holdings_type='electronic')
        else:
            current_app.logger.warning(
                'create document holding no org: {source}'.format(
                    source=provider['provider']
                )
            )
    del (new_record['providers'])
    del (new_record['electronicLocator'])
    return new_record


def update_document_holding(record, pid):
    """Update a document and a holding for a harvested ebook."""
    # harvested_sources = get_harvested_sources(record)
    new_record = None
    providers = record.get('providers', [])
    uri = record.get(
                    'electronicLocator')[0].get('url')
    del (record['providers'])
    del (record['electronicLocator'])
    existing_record = Document.get_record_by_pid(pid)
    new_record = existing_record.replace(
        record,
        dbcommit=True,
        reindex=True
    )
    for holding_pid in Holding.get_holdings_pid_by_document_pid(pid):
        holding = Holding.get_record_by_pid(holding_pid)
        holding.delete(force=False, dbcommit=True, delindex=True)


    for provider in providers:
        org = Organisation.get_record_by_pid(provider['organisation'])
        if org:
            item_type_pid = org.online_circulation_category()
            locations = org.get_online_locations()
            electronic_location = {
                'source': '{provider} - {collection}'.format(
                        provider=provider['provider'],
                        collection=provider['collection']),
                'uri': uri
            }
            for location_pid in locations:
                create_holding(
                    document_pid=new_record.pid,
                    location_pid=location_pid,
                    item_type_pid=item_type_pid,
                    electronic_location=electronic_location,
                    holdings_type='electronic')

        else:
            current_app.logger.warning(
                'create document holding no org: {source}'.format(
                    source=provider['provider']
                )
            )

    return new_record
