# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2022 RERO
# Copyright (C) 2022 UCLouvain
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

"""Document CSL-JSON Schema."""

from invenio_rest.serializer import BaseSchema as Schema
from marshmallow import fields, missing, post_dump, \
    post_load, pre_dump, pre_load, validate, validates, validates_schema, \
    ValidationError

from rero_ils.modules.contributions.utils import \
    get_contribution_localized_value

CREATOR_ROLES = [
    'aut', 'cmp', 'cre', 'dub', 'pht', 'ape', 'aqt', 'arc', 'art', 'aus',
    'chr', 'cll', 'com', 'drt', 'dsr', 'enj', 'fmk', 'inv', 'ive', 'ivr',
    'lbt', 'lsa', 'lyr', 'pra', 'prg', 'rsp', 'scl'
]


def clean_empty(data, keys):
    """Clean empty values."""
    for k in keys:
        if k in data and not data[k]:
            del data[k]
    return data


class BaseDocumentSchema(Schema):
    """Base schema class for document."""

    def get_document_types(self, obj):
        """Return document types."""
        doc_types = []
        metadata = obj['metadata']
        for main_type, subtype in [
            (doc_type.get('main_type'), doc_type.get('subtype'))
                for doc_type in metadata.get('type', [])]:

            if subtype:
                main_type = f'{main_type} / {subtype}'
            doc_types.append(main_type)

        return doc_types

    def get_title(self, obj):
        metadata = obj['metadata']
        """Return first title."""
        return next(
            filter(lambda x: x.get('type') == 'bf:Title',
                   metadata['title'])
        ).get('_text')

    def get_secondary_title(self, obj):
        """Return secondary title."""
        metadata = obj['metadata']
        # return series title if exist
        if 'seriesStatement' in metadata:
            return [
                data['value']
                for serie in metadata.get('seriesStatement', [])
                for data in serie.get('_text', [])
            ]

        # get partOf title
        return [
            part_of_title['value']
            for title in metadata.get('title', [])
            for part_of_title in title.get('partOfTitle', [])
            if 'partOf' in title['type']
        ]

    def get_author(self, obj):
        """Return author."""

        metadata = obj['metadata']

        def _extract_contribution_callback(contribution):
            """Extract value for the given subject."""
            agent = contribution.get('agent', {})
            role = contribution.get('role', [])
            if any(r in role for r in CREATOR_ROLES):
                return self._get_localized_contribution(agent) \
                       or agent.get('preferred_name')

        return [contribution
                for contribution in map(_extract_contribution_callback,
                                        metadata.get('contribution', [])
                                        )
                if contribution]

    def _get_localized_contribution(self, agent):
        """Return localized contribution."""
        # TODO: use default language or custom_language (see baseFormatter)
        key = f'authorized_access_point_en'
        return agent.get(key)

    def get_language(self, obj):
        """Return language."""
        metadata = obj['metadata']
        return [lang.get('value') for lang in metadata.get('language',[])]

    def get_publisher(self, obj):
        """Return publisher."""
        metadata = obj['metadata']
        return [
            data['value']
            for provision in metadata.get('provisionActivity', [])
            for statement in provision.get('statement', [])
            for data in statement.get('label', [])
            if provision['type'] == 'bf:Publication'
            and statement['type'] == 'bf:Agent'
        ]

    def get_publication_place(self, obj):
        """Return city."""
        metadata = obj['metadata']
        return [
            data['value']
            for provision in metadata.get('provisionActivity', [])
            for statement in provision.get('statement', [])
            for data in statement.get('label', [])
            if provision['type'] == 'bf:Publication'
            and statement['type'] == 'bf:Place'
        ]

    def get_volume_number(self, obj):
        """Return volume number."""
        metadata = obj['metadata']
        return [
            numbering['volume']
            for part_of in metadata.get('partOf', [])
            for numbering in part_of.get('numbering', [])
            if 'volume' in numbering
        ]

    def get_issue_number(self, obj):
        """Return issue number."""
        metadata = obj['metadata']
        return [
            numbering['issue']
            for part_of in metadata.get('partOf', [])
            for numbering in part_of.get('numbering', [])
            if 'issue' in numbering
        ]

    def _get_identifier_by_types(self, obj, types):
        """Return identifier for the given types."""
        metadata = obj['metadata']
        return [
            identifier['value']
            for identifier in metadata.get('identifiedBy', [])
            if identifier['type'] in types
        ]

    def get_doi(self, obj):
        """Return DOI."""
        return self._get_identifier_by_types(obj, ['bf:Doi'])

    def get_isbn(self, obj):
        """Return isbn."""
        return self._get_identifier_by_types(obj, ['bf:Isbn'])

    def get_issn(self, obj):
        """Return issn."""
        return self._get_identifier_by_types(obj, ['bf:Issn', 'bf:IssnL'])

    def get_url(self, obj):
        """Return url."""
        metadata = obj['metadata']
        return [
            locator['url']
            for locator in metadata.get('electronicLocator', [])
            if locator['type'] in ['resource', 'versionOfResource']
        ]

    def get_edition(self, obj):
        """Return edition."""
        metadata = obj['metadata']
        return [v.get('_text') for v in metadata.get('editionStatement', [])]

    def get_subjects(self, obj):
        """Return subjects."""

        metadata = obj['metadata']

        def _extract_subject_callback(subject):
            """Extract value for the given subject."""
            if subject:
                subject_type = subject.get('type')
                if subject_type in ['bf:Person',
                                    'bf:Organisation',
                                    'bf:Place']:
                    return get_contribution_localized_value(
                        contribution=subject,
                        key='authorized_access_point',
                        language='en'
                    ) or subject.get('preferred_name')
                if subject_type == 'bf:Work':
                    return '. - '.join([
                        subject.get(key, '')
                        for key in ['creator', 'title']
                        if subject.get(key)
                    ])
                if subject_type in ['bf:Topic', 'bf:Temporal']:
                    return subject.get('term')

        return [subject
                for subject in map(_extract_subject_callback,
                                   metadata.get('subjects', []))
                if subject]

    def get_start_page(self, obj):
        """Return start page."""
        metadata = obj['metadata']
        return [
                   numbering['pages'].split('-')[0]
                   for part_of in metadata.get('partOf', [])
                   for numbering in part_of.get('numbering', [])
                   if 'pages' in numbering
               ] \
            or metadata.get('extent', [])


class DocumentSchemaCSLJSON(BaseDocumentSchema):
    """Schema for documents in CSL-JSON."""

    id = fields.Str(attribute='metadata.pid')
    type = fields.Method('get_document_types')
    title = fields.Method('get_title')
    edition = fields.Method('get_edition')
    #secondary_title = fields.Method('get_secondary_title')
    author = fields.Method('get_author')
    language = fields.Method('get_language')
    publisher = fields.Method('get_publisher')
    publisher_place = fields.Method('get_publication_place')
    keyword = fields.Method('get_subjects')
    volume = fields.Method('get_volume_number')
    issue = fields.Method('get_issue_number')
    page_first = fields.Method('get_start_page')
    DOI = fields.Method('get_doi')
    ISBN = fields.Method('get_isbn')
    ISSN = fields.Method('get_issn')
    URL = fields.Method('get_url')

    # abstract = fields.Str(attribute='metadata.description')
    # issued = fields.Method('get_issue_date')
    #
    # version = fields.Str(attribute='metadata.version')
    # note = fields.Str(attribute='metadata.notes')
    #
    #
    # container_title = fields.Method('get_container_title')
    # page = fields.Method('get_page')

    @post_dump(pass_many=False)
    #    @post_load(pass_original=True)
    def clean(self, data, many, **kwargs):
        """Clean empty values."""
        return clean_empty(data, [
            'page_first', 'ISSN', 'ISBN', 'volume', 'issue', 'DOI', 'URL'])
