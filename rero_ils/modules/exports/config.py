from invenio_records_rest.utils import obj_or_import_string

from rero_ils.modules.permissions import record_permission_factory

item_permission = \
    obj_or_import_string('rero_ils.modules.items.permissions:ItemPermission')

EXPORT_RECORDS_REST_ENDPOINTS = dict(
    inventory=dict(
        search_serializers_aliases={
            'csv': 'text/csv',
        },
        search_serializers={
            'text/csv': (
                'rero_ils.modules.items.serializers:csv_item_search'
            ),
        },
        search_factory_imp='rero_ils.query:items_search_factory',
        list_permission_factory_imp=lambda record: record_permission_factory(
            action='list', record=record, cls=item_permission),
    ),
    documents=dict(

    ),
    orders=dict(

    )
)
