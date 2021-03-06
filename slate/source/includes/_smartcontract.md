# Smart Contract

## Generate multisig_address

### Description
Generate multisig address(`multisig_address`) of the contract by public keys from oracles.

> Sample Request

```json
{
  "sender_address": "1PeUaJHGgjMfrWzTzFnkDVN2VdoHB2CLQb",
  "oracles": "[{"url": "http://smart-contract.vchain.com:7788","name": "Oracle server"}]",
  "m" : "1"
}
```

> Sample Response

```js
{
  "data": {
    "multisig_address": "3HnMCWayuCwXe7ALqa3e9HiU47VDruxJ8Q"
  }
}
```

### HTTP Request

`POST http://<CONTRACT_SERVER_URL>/smart-contract/multisig-addresses/`


### Query Parameters

Field          | Type   | Required | Description
-------------- | ------ | -------- | --------------
sender_address | string | T        | sender address
m              | string | T        | m for m-of-n multisig_address, at least m oracles reach a consensus
oracles        | array  | T        | list of oracles
→ name         | string | T        | name of oracle
→ url          | string | T        | url of oracle

### Return Value

Field            | Type   | Description
---------------- | ------ | --------------
multisig_address | string | multisig_address of oracles' public keys



## Deploy contract

### Description
Prepare a raw transaction of deploying contract to specific `multisig_address`.


> Sample Request

```json
{
  "sender_address": "1PeUaJHGgjMfrWzTzFnkDVN2VdoHB2CLQb",
  "source_code": "contract greeter{ string greeting; function greeter(string _greeting) public { greeting = _greeting; } function greet() constant returns (string) { return greeting; } function setgreeter(string _greeting) public { greeting = _greeting; } }",
  "contract_name" : "1",
  "conditions": "[]",
  "function_inputs": [{"name": "_greeting","type": "string","value": "1234"}]
}
```

> Sample Response

```js
{
  "data": {
    "raw_tx": "01000000018deec0c136e68b53d9796b69e04b8d9fff623b15c969305a286f1f481bd5fb75020000001976a914f8692cef96e01715e556b8f91c713b3daa9ce2c288acffffffff0300e1f5050000000017a914b0842ebbffc1d41b5bcf424771ce3a8e95031fba87010000000000000000000000fda9076a4da5077b226d756c74697369675f61646472223a202233486e4d43576179754377586537414c7161336539486955343756447275784a3851222c2022736f757263655f636f6465223a202236303630363034303532336636313030303035373630343035313631303339323338303338303631303339323833333938313031363034303532383038303531383230313931393035303530356238303630303039303830353139303630323030313930383238303534363030313831363030313136313536313031303030323033313636303032393030343930363030303532363032303630303032303930363031663031363032303930303438313031393238323630316631303631303037323537383035313630666631393136383338303031313738353535363130306130353635623832383030313630303130313835353538323135363130306130353739313832303135623832383131313135363130303966353738323531383235353931363032303031393139303630303130313930363130303834353635623562353039303530363130306335393139303562383038323131313536313030633135373630303038313630303039303535353036303031303136313030613935363562353039303536356235303530356235303562363130326239383036313030643936303030333936303030663330303630363036303430353236303030333537633031303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303039303034363366666666666666663136383036336334353939323762313436313030343935373830363363666165333231373134363130306130353735623631303030303536356233663631303030303537363130303965363030343830383033353930363032303031393038323031383033353930363032303031393038303830363031663031363032303830393130343032363032303031363034303531393038313031363034303532383039333932393139303831383135323630323030313833383338303832383433373832303139313530353035303530353035303931393035303530363130313336353635623030356233663631303030303537363130306164363130316462353635623630343035313830383036303230303138323831303338323532383338313831353138313532363032303031393135303830353139303630323030313930383038333833363030303833313436313030666335373562383035313832353236303230383331313135363130306663353736303230383230313931353036303230383130313930353036303230383330333932353036313030643835363562353035303530393035303930383130313930363031663136383031353631303132383537383038323033383035313630303138333630323030333631303130303061303331393136383135323630323030313931353035623530393235303530353036303430353138303931303339306633356238303630303039303830353139303630323030313930383238303534363030313831363030313136313536313031303030323033313636303032393030343930363030303532363032303630303032303930363031663031363032303930303438313031393238323630316631303631303138323537383035313630666631393136383338303031313738353535363130316230353635623832383030313630303130313835353538323135363130316230353739313832303135623832383131313135363130316166353738323531383235353931363032303031393139303630303130313930363130313934353635623562353039303530363130316435393139303562383038323131313536313031643135373630303038313630303039303535353036303031303136313031623935363562353039303536356235303530356235303536356236303230363034303531393038313031363034303532383036303030383135323530363030303830353436303031383136303031313631353631303130303032303331363630303239303034383036303166303136303230383039313034303236303230303136303430353139303831303136303430353238303932393139303831383135323630323030313832383035343630303138313630303131363135363130313030303230333136363030323930303438303135363130323832353738303630316631303631303235373537363130313030383038333534303430323833353239313630323030313931363130323832353635623832303139313930363030303532363032303630303032303930356238313534383135323930363030313031393036303230303138303833313136313032363535373832393030333630316631363832303139313562353035303530353035303930353035623930353630306131363536323761376137323330353832306665613433643633663738626663393164386234633063306236373562353735386433333930333734633636623534616332636537336335623266633666306130303239222c2022746f5f61646472223a202263613366376634303031653634613139353837623933316537663561336434633734326430306530227d00000000002300f2ff5800001976a914f8692cef96e01715e556b8f91c713b3daa9ce2c288ac010000000000000005000000"
  }
}
```

### HTTP Request

`POST http://<CONTRACT_SERVER_URL>/smart-contract/multisig-addresses/[:multisig_address]/contracts/`

### Query Parameters

Field            | Type     | Required | Description
---------------- | -------- | -------- | ---
sender_address   | string   | T        | sender address
source_code      | string   | T        | source code
contract_name    | string   | T        | contract you want to deploy
conditions       | array    | F        | array of oraclize conditions
→ condition_type | string   | F        | type of condition
→ receiver_addr  | string   | F        | receiver address
→ color          | string   | F        | color of condition
function_inputs  | array    | F        | inputs of constructor function
→ name           | string   | T        | name of parameter
→ type           | string   | T        | type of parameter
→ value          | **type** | T        | value of parameter

### Return Value

Field  | Type    | Description
------ | ------- | -------------
raw_tx | string  | raw transaction


## Get information of the contract object 

### Description
Get the detailed information of the contract.

> Sample Response

```js
{
  "data": [
    {
      "interface": [
        {
          "constant": false,
          "outputs": [],
          "type": "function",
          "name": "setgreeter",
          "inputs": [
            {
              "type": "string",
              "name": "_greeting"
            }
          ],
          "payable": false
        },
        {
          "constant": true,
          "outputs": [
            {
              "type": "string",
              "name": ""
            }
          ],
          "type": "function",
          "name": "greet",
          "inputs": [],
          "payable": false
        },
        {
          "type": "constructor",
          "inputs": [
            {
              "type": "string",
              "name": "_greeting"
            }
          ],
          "payable": false
        }
      ],
      "sender_nonce_predicted": 0,
      "tx_hash_init": "473f03bd780a5ebe3a32f2be918678ddb9990617f60041a560b18f62d65ca7e5",
      "hash_op_return": 2033423023,
      "is_deployed": true,
      "sender_evm_address": "8b82b02cabca8eb30f1f79394ad9f2188ddfbf5c"
    }
  ]
}
```
### HTTP Request

`GET http://<CONTRACT_SERVER_URL>/smart-contract/multisig-addresses/[:multisig_address]/contracts/[:contract_address]/`


### Return Value

Field                  | Type     | Description
---------------------- | -------- | --------------------
interface              | list     | abi
-> constant            | boolean  | constant function or not
-> outputs             | list     | output varaible
-> type                | string   | function or event
-> name                | string   | name of item
-> inputs              | list     | input variable
-> payable             | list     | payable or not
sender_nonce_predicted | int      | for  confirm contract address is double-deployed or not
tx_hash_init           | string   | transaction hash id
hash_op_return         | int      | hash of the `OP_RETURN`
is_deployed            | boolean  | if the contract is deployed or not
sender_evm_address     | string   | sender address in evm environment

## Call function

### Description
1. For constant function, the API would response function_outputs.
2. Otherwise, API would response a raw transaction(`raw_tx`) contains bytecode. The raw_tx need to be sign and send to OSS API.

> Sample Request of constant function call

```json
{
  "sender_address": "1PeUaJHGgjMfrWzTzFnkDVN2VdoHB2CLQb",
  "function_name": "greet",
  "function_inputs": "[]",
  "amount": 0,
  "color": 0
}
```

> Sample Response of constant function call

```js
{
  "data": {
    "out": "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000043536373800000000000000000000000000000000000000000000000000000000",
    "function_outputs": [
      {
        "type": "string",
        "value": "5678"
      }
    ]
  }
}
```

> Sample Request of transaction call

```json
{
  "sender_address": "1PeUaJHGgjMfrWzTzFnkDVN2VdoHB2CLQb",
  "function_name": "setgreeter",
  "function_inputs": "[{"name": "_greeting","type": "string","value": "5678"}]",
  "amount": 0,
  "color": 0
}
```

> Sample Response of transaction call

```js
{
  "data": {
    "raw_tx": "01000000014e4481a8c55e01f73e67a293d80fe4737d8223060bc79ad3173665cce1bd4218020000001976a914f8692cef96e01715e556b8f91c713b3daa9ce2c288acffffffff0300e1f5050000000017a9142142701335f3c3072200bd2fe835077e4f21fcc787010000000000000000000000fd56016a4d52017b2266756e6374696f6e5f696e707574735f68617368223a20226334353939323762303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303032303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303433353336333733383030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030222c20226d756c74697369675f61646472223a20223334697370343250394e6133535331596b5a336759626a71727255336e4e5a575756222c2022746f5f61646472223a202263613366376634303031653634613139353837623933316537663561336434633734326430306530227d0000000000e5ebfdff5800001976a914f8692cef96e01715e556b8f91c713b3daa9ce2c288ac010000000000000005000000"
  }
}
```

### HTTP Request

`POST http://<CONTRACT_SERVER_URL>/smart-contract/multisig-addresses/[:multisig_address]/contracts/[:contract_address]/function/`

### Query Parameters

Field           | Type     | Required | Description
--------------- | -------- | -------- | ---------------
sender_address  | string   | T        | sender address
function_name   | string   | T        | function name
function_inputs | array    | T        | function input list
→ name          | string   | T        | name of parameter
→ type          | string   | T        | type of parameter
→ value         | **type** | T        | value of parameter
color           | string   | T        | token
amount          | string   | T        | amount of value of specific color token


### Return Value for `1. constant function call`

Field            | Type     | Description
---------------- | -------- | -------------------
out              | string   | output bytecode
function_outputs | array    | array of decoded function outputs data
→ type           | string   | type of value
→ value          | **type** |  value

### Return Value for `2. transaction call`

Field           | Type     | Description
--------------- | -------- | ---------------
raw_tx          | string   | raw transaction

## Get contract abi

### Description
Get the function_list and event_list of the contract.

> Sample Response

```js
{
  "data": {
    "event_list": [],
    "function_list": [
      {
        "outputs": [],
        "type": "function",
        "name": "setgreeter",
        "inputs": [
          {
            "type": "string",
            "name": "_greeting"
          }
        ]
      },
      {
        "outputs": [
          {
            "type": "string",
            "name": ""
          }
        ],
        "type": "function",
        "name": "greet",
        "inputs": []
      }
    ]
  }
}
```
### HTTP Request

`GET http://<CONTRACT_SERVER_URL>/smart-contract/multisig-addresses/[:multisig_address]/contracts/[:contract_address]/function/`


### Return Value

Field         | Type    | Description
------------- | ------- | -------------
event_list    | list    | event abi
-> type       | string  | event
-> name       | string  | name
-> inputs     | list    | inputs variable
---> type     | string  | type of inputs variable
---> name     | string  | name of inputs variable
function_list | list    | function abi
-> type       | string  | constructor or function
-> name       | string  | name of function
-> inputs     | list    | input variable
---> type     | string  | type of input variable
---> name     | string  | name of input variable
-> outputs    | list    | output variable
---> type     | string  | type of output variable

## Bind contract interface

### Description
Bind contract-created contract to specific interface.
The contract-created contract is created in VM state, but lack of interface in Database. Use this API can help to bind a known contract ABI to contract-created contract.

> Sample Request

```json
{
  "new_contract_address": "56f32d84a9b41607048641d1d9ada884bab51dbd",
  "original_contract_address": "823a859e21671074fe844bf44399985e8b8be99f"
}
```

> Sample Response

```js
{
  "data": {
    "is_success": true
  }
}
```

### HTTP Request
`POST http://<CONTRACT_SERVER_URL>/smart-contract/multisig-addresses/[:multisig_address]/bind/`

### Query Parameters

Field                     | Type   | Required | Description
------------------------- | ------ | -------- | ---------------
new_contract_address      | string | T        | contract-created contract address
original_contract_address | string | T        | original contract address


### Return Value

Field      | Type | Description
---------- | ---- | ---------------
is_success | bool | binding is successful or failed
