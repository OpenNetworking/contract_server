import json
import time
from binascii import hexlify
from subprocess import check_call
from gcoin import *

from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.views.generic.edit import BaseFormView

import base58
from rest_framework import status
from rest_framework.views import APIView
import gcoinrpc
from app.models import Proposal, Registration, Keystore, OraclizeContract, ProposalOraclizeLink
from app.serializers import ProposalSerializer, RegistrationSerializer
from .deploy_contract_utils import *
from .forms import SignForm
from oracle.mixins import CsrfExemptMixin

try:
    import http.client as httplib
except ImportError:
    import httplib

EVM_PATH = '../oracle/states/{multisig_address}'


def wallet_address_to_evm(address):
    address = base58.b58decode(address)
    address = hexlify(address)
    address = hash160(address)
    return address


class Proposes(APIView):
    """
    Give the publicKey when invoked.
    """
    def post(self, request):
        # Return public key to Contract-Server
        body_unicode = request.body.decode('utf-8')

        json_data = json.loads(body_unicode)
        try:
            source_code = json_data['source_code']
            conditions = json_data['conditions']
        except:
            response = {'status': 'worng argument'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

        private_key = sha256(get_random_string(64, '0123456789abcdef'))
        public_key = privtopub(private_key)
        address = pubtoaddr(public_key)
        p = Proposal(source_code=source_code, public_key=public_key, address=address)
        k = Keystore(public_key=public_key, private_key=private_key)
        p.save()
        k.save()

        for condition in conditions:
            if condition['condition_type'] == 'specifies_balance' or condition['condition_type'] == 'issuance_of_asset_transfer':
                o = OraclizeContract.objects.get(name=condition['condition_type'])
                l = ProposalOraclizeLink.objects.create(receiver=condition['receiver_addr'], color=condition['color_id'], oraclize_contract=o)
                p.links.add(l)
            else:
                o = OraclizeContract.objects.get(name=condition['condition_type'])
                l = ProposalOraclizeLink.objects.create(receiver='0', color='0', oraclize_contract=o)
                p.links.add(l)

        response = {'public_key': public_key}
        return JsonResponse(response, status=httplib.OK)


class Multisig_addr(APIView):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        try:
            pubkey = json_data['pubkey']
            multisig_addr = json_data['multisig_addr']
        except:
            response = {'status': 'worng argument'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

        p = Proposal.objects.get(public_key=pubkey)
        p.multisig_addr = multisig_addr
        p.save()
        response = {
            "status": "success"
        }
        return JsonResponse(response)


class Registrate(APIView):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        json_data = json.loads(body_unicode)

        try:
            public_key = json_data['public_key']
            p = Proposal.objects.get(public_key=json_data['public_key'])
            multisig_address = json_data['multisig_address']
            redeem_script = json_data['redeem_script']
            r = Registration(proposal=p, multisig_address=multisig_address,
                             redeem_script=redeem_script)
            r.save()
        except:
            response = {'status': 'worng argument'}
            return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="aplication/json")


class Sign(CsrfExemptMixin, BaseFormView):
    http_method_name = ['post']
    form_class = SignForm

    def form_valid(self, form):
        tx = form.cleaned_data['tx']
        script = form.cleaned_data['script']
        input_index = form.cleaned_data['input_index']
        user_address = form.cleaned_data['user_address']
        multisig_address = form.cleaned_data['multisig_address']
        amount = form.cleaned_data['amount']
        color_id = form.cleaned_data['color_id']

        user_evm_address = wallet_address_to_evm(user_address)
        # need to check contract result before sign Tx
        try:
            with open(EVM_PATH.format(multisig_address=multisig_address), 'r') as f:
                content = json.load(f)
                account = content['accounts'][user_evm_address]
                if not account:
                    response = {'error': 'Address not found'}
                    return JsonResponse(response, status=httplib.NOT_FOUND)
                account_amount = account['balance'][color_id]
        except IOError:
            # Log
            response = {'error': 'contract not found'}
            return JsonResponse(response, status=httplib.INTERNAL_SERVER_ERROR)
        if int(account_amount) < int(amount):
            response = {'error': 'insufficient funds'}
            return JsonResponse(response, status=httplib.BAD_REQUEST)

        #signature = connection.signrawtransaction(tx)
        p = Proposal.objects.get(multisig_addr=multisig_address)
        private_key = Keystore.objects.get(public_key=p.public_key).private_key

        signature = multisign(tx, input_index, script, private_key)
        # return only signature hex
        response = {'signature': signature}

        return JsonResponse(response, status=httplib.OK)

    def form_invalid(self, form):
        response = {'error': form.errors}

        return JsonResponse(response, status=httplib.BAD_REQUEST)


class ProposalList(APIView):

    def get(self, request):
        proposals = Proposal.objects.all()
        serializer = ProposalSerializer(proposals, many=True)
        response = {'proposal': serializer.data}
        return HttpResponse(json.dumps(response), content_type="application/json")


class RegistrationList(APIView):

    def get(self, request):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        response = {'registration': serializer.data}
        return HttpResponse(json.dumps(response), content_type="application/json")


class GetBalance(APIView):

    def get(self, request, multisig_address, address):
        user_evm_address = wallet_address_to_evm(address)
        try:
            with open(EVM_PATH.format(multisig_address=multisig_address), 'r') as f:
                content = json.load(f)
                account = content['accounts'][user_evm_address]
                amount = account['balance']
                response = amount
                return JsonResponse(response, status=httplib.OK)
        except:
            response = {}
            return JsonResponse(response, status=httplib.OK)


class GetStorage(APIView):

    def get(self, request, multisig_address):
        contract_evm_address = wallet_address_to_evm(multisig_address)
        try:
            with open(EVM_PATH.format(multisig_address=multisig_address), 'r') as f:
                content = json.load(f)
                account = content['accounts'][contract_evm_address]
                storage = account['storage']
                response = storage
                return JsonResponse(response, status=httplib.OK)
        except:
            response = {}
            return JsonResponse(response, status=httplib.OK)

class DumpContractState(APIView):
    """
    Get contract state file
    """
    def get(self, request, multisig_address):
        contract_evm_address = wallet_address_to_evm(multisig_address)
        try:
            with open(EVM_PATH.format(multisig_address=multisig_address), 'r') as f:
                content = json.load(f)
                response = content
                return JsonResponse(response, status=httplib.OK)
        except:
            response = {}
            return JsonResponse(response, status=httplib.OK)

class CheckContractCode(APIView):

    def get(self, request, multisig_address):
        contract_evm_address = wallet_address_to_evm(multisig_address)
        try:
            with open(EVM_PATH.format(multisig_address=multisig_address), 'r') as f:
                content = json.load(f)
                account = content['accounts'][contract_evm_address]
                code = account['code']
                response = {'code': code}
                return JsonResponse(response, status=httplib.OK)
        except:
            response = {'status': 'Contract code not found'}
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


class NewTxNotified(APIView):

    def post(self, request, tx_hash):
        response = {}
        print('Received notify with tx_hash ' + tx_hash)
        deploy_contracts(tx_hash)

        response['data'] = 'ok, received notify with tx_hash ' + tx_hash
        return JsonResponse(response, status=httplib.OK)

class OraclizeContractInterface(APIView):

    def get(self, request, contract_name):
        response = {}

        obj = OraclizeContract.objects.get(name=contract_name)
        response = {
            'address': obj.address,
            'interface': obj.interface,
        }
        return JsonResponse(response, status=httplib.OK)
