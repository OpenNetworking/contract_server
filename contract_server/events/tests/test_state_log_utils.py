import os
import json
import mock

from django.test import TestCase
from events import state_log_utils
from events.models import Watch
from contracts.models import MultisigAddress, Contract

EVENT_NAME = "TestEvent"


class StateLogUtilsTest(TestCase):

    def fake_subscribe_address_notification(self, multisig_address, callback_url):
        subscription_id = '1'
        created_time = '2017-03-15'
        return subscription_id, created_time

    @mock.patch("gcoinapi.client.GcoinAPIClient.subscribe_address_notification", fake_subscribe_address_notification)
    def setUp(self):
        self.logs = [{
            "address": "bd841c963c498133d26596859144042ae186738f",
            "topics": [
                "0x4786b80b6e9293ff9558bf352de8b5a7cb015fcca7e59d13b3a1615225d9cd71",
                "0x0000000000000000000000000000000000000000000000000000000000001234",
                "0x0000000000000000000000000000000000000000000000000000000000000171"
            ],
            "data": "000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001a011340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003039ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff85000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000b68656c6c6f20776f726c64000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002355660000000000000000000000000012556600000000000000000000000000124525440000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000001570000000000000000000000000000000000000000000000000000000000000158",
            "transactionHash": "0000000000000000000000000000000000000000000000000000000000000000",
            "transactionIndex": 0,
            "blockHash": "0000000000000000000000000000000000000000000000000000000000000000",
            "logIndex": 0
        }]

        self.log = self.logs[0]

        # Watch object
        source_code = 'pragma solidity ^0.4.7;contract encodeAndDecode {string my_string = "init";bytes my_bytes;bytes2 my_bytes2;bytes32 my_bytes32;uint my_uint;int my_int;bool my_bool;address my_address;address [] my_address_array_dynamic;int [2][2] my_int_array_2d;event TestEvent(string event_string,bytes  event_bytes,bytes2 event_bytes2,bytes32 indexed event_bytes32,uint event_uint,int event_int,bool event_bool,address indexed event_address,address [] event_address_array_dynamic,int [2][2] event_int_array_2d);function encodeAndDecode(string _string,bytes _bytes, bytes2 _bytes2, bytes32 _bytes32,uint _uint, int _int,bool _bool, address _address) public {my_string = _string;my_bytes = _bytes;my_bytes2 = _bytes2;my_bytes32 = _bytes32;my_uint = _uint;my_int = _int;my_bool = _bool;my_address = _address;my_bytes32 = 0x1234;my_address_array_dynamic.push(0x0000000000000000000000000000000000000157);my_address_array_dynamic.push(0x0000000000000000000000000000000000000158);my_int_array_2d = [[1, 2],[3, 4]];}function testEvent() public {TestEvent(my_string,my_bytes, my_bytes2, my_bytes32,my_uint, my_int,my_bool, my_address,my_address_array_dynamic,my_int_array_2d);}function getAttributes() constant returns (string,bytes, bytes2, bytes32,uint,int,bool, address,address[],int[2][2]) {return (my_string,my_bytes, my_bytes2, my_bytes32,my_uint, my_int,my_bool, my_address,my_address_array_dynamic,my_int_array_2d);}}'
        self.multisig_address = '3By64hdBQ6cYh34ucqW6Dsv9ctiuX2krcn'
        self.multisig_script = 'multisig_script'
        interface = '[{"outputs": [{"name": "", "type": "string"}, {"name": "", "type": "bytes"}, {"name": "", "type": "bytes2"}, {"name": "", "type": "bytes32"}, {"name": "", "type": "uint256"}, {"name": "", "type": "int256"}, {"name": "", "type": "bool"}, {"name": "", "type": "address"}, {"name": "", "type": "address[]"}, {"name": "", "type": "int256[2][2]"}], "name": "getAttributes", "inputs": [], "constant": true, "payable": false, "type": "function"}, {"outputs": [], "name": "testEvent", "inputs": [], "constant": false, "payable": false, "type": "function"}, {"inputs": [{"name": "_string", "type": "string"}, {"name": "_bytes", "type": "bytes"}, {"name": "_bytes2", "type": "bytes2"}, {"name": "_bytes32", "type": "bytes32"}, {"name": "_uint", "type": "uint256"}, {"name": "_int", "type": "int256"}, {"name": "_bool", "type": "bool"}, {"name": "_address", "type": "address"}], "payable": false, "type": "constructor"},{"name": "TestEvent", "inputs": [{"name": "event_string", "indexed": false, "type": "string"}, {"name": "event_bytes", "indexed": false, "type": "bytes"}, {"name": "event_bytes2", "indexed": false, "type": "bytes2"}, {"name": "event_bytes32", "indexed": true, "type": "bytes32"}, {"name": "event_uint", "indexed": false, "type": "uint256"}, {"name": "event_int", "indexed": false, "type": "int256"}, {"name": "event_bool", "indexed": false, "type": "bool"}, {"name": "event_address", "indexed": true, "type": "address"}, {"name": "event_address_array_dynamic", "indexed": false, "type": "address[]"}, {"name": "event_int_array_2d", "indexed": false, "type": "int256[2][2]"}], "type": "event", "anonymous": false}]'

        multisig_address_object = MultisigAddress.objects.create(
            address=self.multisig_address,
            script=self.multisig_script)

        contract = Contract.objects.create(
            state_multisig_address=multisig_address_object,
            contract_address="bd841c963c498133d26596859144042ae186738f",
            source_code=source_code,
            color=1,
            amount=0,
            interface=interface)

        Watch.objects.create(
            event_name=EVENT_NAME,
            contract=contract
        )

        Watch.objects.create(
            event_name=EVENT_NAME,
            contract=contract,
            conditions=str([{"value": "hello world", "type": "string", "name": "event_string"}])
        )

        Watch.objects.create(
            event_name=EVENT_NAME,
            contract=contract,
            conditions=str([{"value": "NOT MATCHING", "type": "string", "name": "event_string"}])
        )

    def test_decode_logs(self):
        watch = Watch.objects.filter(event_name=EVENT_NAME)[0]

        event = state_log_utils._decode_log(self.log, watch)
        expect_event = {
            'args': [
                {'value': 'hello world', 'type': 'string', 'name': 'event_string', 'indexed': False},
                {'value': '0x5566000000000000000000000000001255660000000000000000000000000012452544', 'type': 'bytes', 'name': 'event_bytes', 'indexed': False},
                {'value': '0x1134', 'type': 'bytes2', 'name': 'event_bytes2', 'indexed': False},
                {'value': '0x0000000000000000000000000000000000000000000000000000000000001234',
                    'type': 'bytes32', 'name': 'event_bytes32', 'indexed': True},
                {'value': 12345, 'type': 'uint256', 'name': 'event_uint', 'indexed': False},
                {'value': -123, 'type': 'int256', 'name': 'event_int', 'indexed': False},
                {'value': True, 'type': 'bool', 'name': 'event_bool', 'indexed': False}, {
                    'value': '0000000000000000000000000000000000000171', 'type': 'address', 'name': 'event_address', 'indexed': True},
                {'value': ['0000000000000000000000000000000000000157', '0000000000000000000000000000000000000158'],
                    'type': 'address[]', 'name': 'event_address_array_dynamic', 'indexed': False},
                {'value': [[1, 2], [3, 4]], 'type': 'int256[2][2]',
                    'name': 'event_int_array_2d', 'indexed': False}
            ]
        }
        self.assertEqual(event['args'], expect_event['args'])

    def test_search_watch(self):
        matching_watch_list = state_log_utils._search_watch(
            self.logs, "3By64hdBQ6cYh34ucqW6Dsv9ctiuX2krcn")

        self.assertEqual(len(matching_watch_list), 2)

    def test_check_watch(self):
        tx_hash = "TEST_TX_HASH"
        log_path = os.path.dirname(os.path.abspath(__file__)) + \
            '/../../states/' + self.multisig_address + "_" + tx_hash + "_log"
        logs_str = json.dumps({"logs": self.logs})
        with open(log_path, 'w+') as f:
            f.write(logs_str)
        matching_watch_list = state_log_utils.check_watch(tx_hash, self.multisig_address)
        self.assertEqual(len(matching_watch_list), 2)

    def test_is_condition_matching(self):
        condition = {
            "name": "condition",
            "type": "uint256",
            "value": 1
        }
        arg = {
            "name": "condition",
            "type": "uint256",
            "value": 1
        }
        is_match = state_log_utils._is_condition_matching(condition, arg)
        self.assertTrue(is_match)

        condition = {
            "name": "not_this_condition",
            "type": "uint256",
            "value": 1
        }
        is_match = state_log_utils._is_condition_matching(condition, arg)
        self.assertTrue(is_match)

        condition = {
            "name": "condition",
            "type": "uint256",
            "value": 2
        }
        is_match = state_log_utils._is_condition_matching(condition, arg)
        self.assertFalse(is_match)

    def test_is_conditions_matching(self):
        conditions_list = [
            {
                "name": "condition1",
                "type": "uint256",
                "value": 1
            },
            {
                "name": "condition2",
                "type": "string",
                "value": "hello"
            }
        ]

        args = [
            {
                "name": "condition1",
                "type": "uint256",
                "value": 1
            },
            {
                "name": "condition2",
                "type": "string",
                "value": "hello"
            }
        ]

        is_match = state_log_utils._is_conditions_matching(conditions_list, args)
        self.assertTrue(is_match)

        def test_check_event_interface(self):
            watch = Watch.objects.filter(event_name=EVENT_NAME)[0]
            topic_0 = "0x4786b80b6e9293ff9558bf352de8b5a7cb015fcca7e59d13b3a1615225d9cd71"
            self.assertTrue(state_log_utils._check_event_interface(watch, topic_0))
