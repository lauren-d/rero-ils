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

"""Mixin helper class."""

from rero_ils.modules.contributions.utils import \
    get_contribution_localized_value

CREATOR_ROLES = [
    'aut', 'cmp', 'cre', 'dub', 'pht', 'ape', 'aqt', 'arc', 'art', 'aus',
    'chr', 'cll', 'com', 'drt', 'dsr', 'enj', 'fmk', 'inv', 'ive', 'ivr',
    'lbt', 'lsa', 'lyr', 'pra', 'prg', 'rsp', 'scl'
]


class BaseDocumentFormatterMixin:
    """Base formatter class."""

    def __init__(self, record):
        """Initialize RIS formatter with the specific record."""
        self.record = record

    def format(self):
        """Return RIS export for single record."""
        raise NotImplementedError

    def _get_document_types(self):
        """Return document types."""
        doc_types = []
        for main_type, subtype in [
            (doc_type.get('main_type'), doc_type.get('subtype'))
                for doc_type in self.record['type']]:

            if subtype:
                main_type = f'{main_type} / {subtype}'
            doc_types.append(main_type)

        return doc_types

    def _get_pid(self):
        """Return reference id."""
        return self.record['pid']

    def _get_title(self):
        """Return first title."""
        return next(
            filter(lambda x: x.get('type') == 'bf:Title',
                   self.record.get('title'))
        ).get('_text')

    def _get_secondary_title(self):
        """Return secondary title."""
        # return series title if exist
        if 'seriesStatement' in self.record:
            return [
                data['value']
                for serie in self.record.get('seriesStatement', [])
                for data in serie.get('_text', [])
            ]

        # get partOf title
        return [
            part_of_title['value']
            for title in self.record.get('title', [])
            for part_of_title in title.get('partOfTitle', [])
            if 'partOf' in title['type']
        ]

    def _get_localized_contribution(self, agent):
        """Return localized contribution."""
        key = f'authorized_access_point_{self._language}'
        return agent.get(key)

    def _get_author(self):
        """Return author."""

        def _extract_contribution_callback(contribution):
            """Extract value for the given subject."""
            agent = contribution.get('agent', {})
            role = contribution.get('role', [])
            if any(r in role for r in CREATOR_ROLES):
                return self._get_localized_contribution(agent) \
                       or agent.get('preferred_name')

        return [contribution
                for contribution in map(_extract_contribution_callback,
                                        self.record.get('contribution', [])
                                        )
                if contribution]

    def _get_secondary_author(self):
        """Return other author."""

        def _extract_contribution_callback(contribution):
            """Extract value for the given contribution."""
            agent = contribution.get('agent', {})
            role = contribution.get('role', [])
            if not any(r in role for r in CREATOR_ROLES):
                return self._get_localized_contribution(agent) \
                       or agent.get('preferred_name')

        return [contribution
                for contribution in map(_extract_contribution_callback,
                                        self.record.get('contribution', [])
                                        )
                if contribution]

    def _get_publication_year(self):
        """Return date."""
        for start_date, end_date in [
            (provision.get('startDate', ''), provision.get('endDate'))
            for provision in self.record.get('provisionActivity', [])
            if provision['type'] == 'bf:Publication'
                and any(label in provision
                        for label in ['startDate', 'endDate'])]:
            if end_date:
                start_date = f'{start_date} - {end_date}'
            # return only the first date
            return start_date

    def _get_start_page(self):
        """Return start page."""
        return [
                   numbering['pages'].split('-')[0]
                   for part_of in self.record.get('partOf', [])
                   for numbering in part_of.get('numbering', [])
                   if 'pages' in numbering
               ] \
            or [self.record['extent']] if self.record.get('extent') else []

    def _get_end_page(self):
        """Return end page."""
        return [
            numbering['pages'].split('-')[1]
            for part_of in self.record.get('partOf', [])
            for numbering in part_of.get('numbering', [])
            if 'pages' in numbering
               and '-' in numbering['pages']
        ]

    def _get_publication_place(self):
        """Return city."""
        return [
            data['value']
            for provision in self.record.get('provisionActivity', [])
            for statement in provision.get('statement', [])
            for data in statement.get('label', [])
            if provision['type'] == 'bf:Publication'
            and statement['type'] == 'bf:Place'
        ]

    def _get_language(self):
        """Return language."""
        if 'language' in self.record:
            return [lang.get('value') for lang in self.record['language']]

    def _get_publisher(self):
        """Return publisher."""
        return [
            data['value']
            for provision in self.record.get('provisionActivity', [])
            for statement in provision.get('statement', [])
            for data in statement.get('label', [])
            if provision['type'] == 'bf:Publication'
            and statement['type'] == 'bf:Agent'
        ]

    def _get_isbn_or_issn(self):
        """Return isbn or issn."""
        return [
            identifier['value']
            for identifier in self.record.get('identifiedBy', [])
            if identifier['type'] in ['bf:Isbn', 'bf:Issn', 'bf:IssnL']
        ]

    def _get_url(self):
        """Return url."""
        return [
            locator['url']
            for locator in self.record.get('electronicLocator', [])
            if locator['type'] in ['resource', 'versionOfResource']
        ]

    def _get_subject(self):
        """Return keyword."""

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
                                   self.record.get('subjects', []))
                if subject]

    def _get_edition(self):
        """Return edition."""
        if 'editionStatement' in self.record:
            return [v.get('_text') for v in self.record['editionStatement']]

    def _get_doi(self):
        """Return DOI."""
        return [
            identifier['value']
            for identifier in self.record.get('identifiedBy', [])
            if identifier['type'] == 'bf:Doi'
        ]

    def _get_volume_number(self):
        """Return volume number."""
        return [
            numbering['volume']
            for part_of in self.record.get('partOf', [])
            for numbering in part_of.get('numbering', [])
            if 'volume' in numbering
        ]

    def _get_issue_number(self):
        """Return issue number."""
        return [
            numbering['issue']
            for part_of in self.record.get('partOf', [])
            for numbering in part_of.get('numbering', [])
            if 'issue' in numbering
        ]
