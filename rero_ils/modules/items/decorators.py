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

"""Decorators about items."""

from functools import wraps

from flask import current_app, jsonify
from invenio_circulation.errors import CirculationException
from invenio_records_rest.utils import obj_or_import_string

from rero_ils.modules.libraries.api import Library
from rero_ils.modules.loans.api import Loan, \
    get_request_by_item_pid_by_patron_pid
from rero_ils.modules.loans.models import LoanAction


def add_action_parameters_and_flush_indexes(function):
    """Add missing action and validate parameters.

    For each circulation action, this method ensures that all required
    parameters are given. Adds missing parameters if any. Ensures the right
    loan transition for the given action.
    """
    @wraps(function)
    def wrapper(item, *args, **kwargs):
        """Executed before loan action."""
        checkin_loan = None
        if function.__name__ == 'validate_request':
            # checks if the given loan pid can be validated
            item.prior_validate_actions(**kwargs)
        elif function.__name__ == 'checkin':
            # the smart checkin requires extra checks/actions before a checkin
            loan, kwargs = item.prior_checkin_actions(**kwargs)
            checkin_loan = loan
        # CHECKOUT: Case where no loan PID
        elif function.__name__ == 'checkout' and not kwargs.get('pid'):
            patron_pid = kwargs['patron_pid']
            item_pid = item.pid
            request = get_request_by_item_pid_by_patron_pid(
                item_pid=item_pid, patron_pid=patron_pid)
            if request:
                kwargs['pid'] = request.pid
        elif function.__name__ == 'extend_loan':
            loan, kwargs = item.prior_extend_loan_actions(**kwargs)
            checkin_loan = loan

        loan, kwargs = item.complete_action_missing_params(
                item=item, checkin_loan=checkin_loan, **kwargs)
        Loan.check_required_params(function.__name__, **kwargs)
        print('ici:', item, 'args:', args, 'kargs:', kwargs)
        item, action_applied = function(item, loan, *args, **kwargs)
        item.change_status_commit_and_reindex()
        return item, action_applied
    return wrapper


def check_operation_allowed(action):
    """Check if a specific action is allowed on an item.

    Check if an 'override_blocking' parameter is present. If this param is
    present and set to True (or corresponding True values [1, 'true', ...])
    then no CIRCULATION_ACTIONS_VALIDATION should be tested.
    Remove this parameter from the data arguments.

    Check the CIRCULATION_ACTIONS_VALIDATION configuration file and execute
    function corresponding to the action specified. All function are execute
    until one return False (action denied) or all actions are successful.

    :param action: the action to check as ItemCirculationAction part.
    :raise CirculationException if a function disallow the operation.
    """
    def inner_function(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            override_blocking = kwargs.pop('override_blocking', False)
            override_blocking = bool(override_blocking)
            if not override_blocking:
                actions = current_app.config.get(
                    'CIRCULATION_ACTIONS_VALIDATION', {})
                for func_name in actions.get(action, []):
                    func_callback = obj_or_import_string(func_name)
                    can, reasons = func_callback(args[0], **kwargs)
                    if not can:
                        raise CirculationException(description=reasons[0])
            return func(*args, **kwargs)
        return decorated_view
    return inner_function


def add_rfid_action(function):
    """Add RFID action.

    This method checks if RFID provider exits for the current library
    transaction. Adds action if RFID provider is defined.
    """
    @wraps(function)
    def decorated_view(*args, **kwargs):
        """Executed after loan action."""

        print('================= ENTRY ADD_RFID_PROVIDER =============')
        from pprint import pprint
        pprint(args)
        print('kwargs ==>')
        pprint(kwargs)
        print(f'action: {function.__name__}')
        # TODO: Check if response is not a tuple => an exception is raised
        #   in do_item_jsonify_action decorator
        results = function(*args, **kwargs)
        print('post processing')
        pprint(results)
        if type(results) is not tuple:
            # get action applied
            print('action_applied')
            pprint(results.json.get('action_applied'))
            if action_applied := results.json.get('action_applied'):
                action = function.__name__
                from datetime import datetime
                start = datetime.now()
                pprint(action_applied)
                if data := action_applied.get(
                        action, action_applied.get(LoanAction.RECEIVE)):
                    loan = Loan(data)
                    pprint(loan)
                    transaction_library_pid = loan.transaction_library_pid
                    library = Library.get_record_by_pid(transaction_library_pid)
                    # check if rfid is enabled for the transaction library
                    if rfid_setting := library.get('rfid_settings'):
                        json_data = results.json
                        provider = rfid_provider_factory(rfid_setting.get('provider'))
                        item = json_data['metadata']
                        json_data.update(
                            {
                                'next_actions': {
                                    action: {
                                        'type': 'http',
                                        'method': 'post',
                                        'uri': rfid_setting.get('service_uri'),
                                        'data': provider.get_rfid_tag_trigger(
                                            action=action,
                                            item_barcode=item.get('barcode')
                                        )
                                    }
                                }
                            }
                        )
                        pprint(results.json)
                        delta = datetime.now() - start
                        print(f'rfid time processing: {delta}')
                        print('================= EXIT ADD_RFID_PROVIDER =============')
                        return jsonify(json_data)

        print('================= EXIT ADD_RFID_PROVIDER =============')
        return results
    return decorated_view


def rfid_provider_factory(provider):
    if provider == 'bibliotheca':
        return BibliothecaRFIDProvider(provider)


class RFIDProvider:
    """RFID provider class."""

    def __init__(self, provider):
        """Constructor."""
        config = current_app.config \
            .get('RERO_ILS_RFID_PROVIDER').get(provider)
        self.tags_status_trigger = config.get('tags_status_trigger', {})


class BibliothecaRFIDProvider(RFIDProvider):
    """Bibliotheca RFID provider class."""

    def get_rfid_tag_trigger(self, action, item_barcode):
        """."""
        return {
            'tagId': item_barcode,
            'IsSecurised': self.tags_status_trigger.get(action, True)
        }
