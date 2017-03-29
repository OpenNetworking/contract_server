try:
    import http.client as httplib
except ImportError:
    import httplib
from rest_framework.views import APIView

from evm_manager import deploy_contract_utils

from contract_server import ERROR_CODE, error_response, data_response
from .decorators import handle_uncaught_exception, handle_apiversion_apiview
from .forms import NotifyForm


class NewTxNotified(APIView):
    @handle_uncaught_exception
    def post(self, request, tx_hash):
        """ Receive Transaction Notification From OSS

        Args:
            tx_hash: the latest tx_hash of multisig_address
            subscription_id: subscription_id of OSS
            notification_id: notification_id of subscription_id

        Returns:
            status: State-Update is failed or completed
        """
        response = {}
        print('Received notify with tx_hash ' + tx_hash)

        completed = deploy_contract_utils.deploy_contracts(tx_hash)
        if completed is False:
            response['status'] = 'State-Update failed: tx_hash = ' + tx_hash
            return data_response(response)

        # response = clear_evm_accouts(multisig_address)
        response['status'] = 'State-Update completed: tx_hash = ' + tx_hash
        return data_response(response)


class AddressNotified(APIView):
    @handle_apiversion_apiview
    def post(self, request, multisig_address):
        """ Receive Address Notification From OSS

        Args:
            multisig_address: multisig_address for contracts
            tx_hash: the latest tx_hash of multisig_address
            subscription_id: subscription_id of OSS
            notification_id: notification_id of subscription_id

        Returns:
            status: State-Update is failed or completed
        """

        form = NotifyForm(request.POST)
        tx_hash = ""

        if form.is_valid():
            tx_hash = form.cleaned_data['tx_hash']
        else:
            response = {"error": form.errors}
            return error_response(httplib.NOT_ACCEPTABLE, form.errors, ERROR_CODE['invalid_form_error'])

        response = {}
        print('Received notify with tx_hash ' + tx_hash)
        completed = deploy_contract_utils.deploy_contracts(tx_hash)
        if completed is False:
            response['status'] = 'State-Update failed: tx_hash = ' + tx_hash
            return data_response(response)

        # response = clear_evm_accouts(multisig_address)
        response['status'] = 'State-Update completed: tx_hash = ' + tx_hash
        return data_response(response)
