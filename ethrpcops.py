'''
sonicskye@2020

Ethereum's web3 operations using webpy library

documentation: https://web3py.readthedocs.io/

EtH JSON-RPC API reference https://eth.wiki/json-rpc/API
'''


from web3 import Web3
from web3.auto.gethdev import w3 as Web3auto
import fire
import json
# geth-poa
# https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
from web3.middleware import geth_poa_middleware
from ethereum import (
    block,
    messages,
    transactions,
    utils
)
from eth_utils import to_bytes, to_hex, to_int, remove_0x_prefix, to_checksum_address


def getlatestblock(provider='http://127.0.0.1:8545', poa=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    # add middleware for POA
    # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # https://web3py.readthedocs.io/en/stable/examples.html
    # this results in AttributeDic
    # which should be converted into JSON by using the built-in web3.toJSON
    # refer to https://github.com/ethereum/web3.py/issues/782
    #data = web3.toJSON(web3.eth.getBlock('latest'))
    data = web3.eth.getBlock('latest')
    return data


def getblockbyheight(height=1, provider='http://127.0.0.1:8545', poa=False, tojson=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    # add middleware for POA
    # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # https://web3py.readthedocs.io/en/stable/examples.html
    data = web3.eth.getBlock(height)
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)

    return data


def getblocknumber(provider='http://127.0.0.1:8545', poa=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    # add middleware for POA
    # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # https://web3py.readthedocs.io/en/stable/examples.html
    # this results in AttributeDic
    # which should be converted into JSON by using the built-in web3.toJSON
    # refer to https://github.com/ethereum/web3.py/issues/782
    #data = web3.toJSON(web3.eth.blockNumber)
    data = web3.eth.blockNumber

    return data

'''
{"currentBlock": 10570480, "highestBlock": 10570591, "knownStates": 121927292, "pulledStates": 121716060, "startingBlock": 5875364}
'''
def getsyncing(provider='http://127.0.0.1:8545', poa=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    # add middleware for POA
    # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # https://web3py.readthedocs.io/en/stable/examples.html
    # this results in AttributeDic
    # which should be converted into JSON by using the built-in web3.toJSON
    # refer to https://github.com/ethereum/web3.py/issues/782
    #data = json.loads(web3.toJSON(web3.eth.syncing))
    data = web3.eth.syncing
    return data


def getchainid(provider='http://127.0.0.1:8545', poa=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    # add middleware for POA
    # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # https://web3py.readthedocs.io/en/stable/examples.html
    # this results in AttributeDic
    # which should be converted into JSON by using the built-in web3.toJSON
    # refer to https://github.com/ethereum/web3.py/issues/782
    #data = json.loads(web3.toJSON(web3.eth.syncing))
    data = web3.eth.chainId
    return data


def getblockcount(provider='http://127.0.0.1:8545', poa=False):
    data = getsyncing(provider, poa)
    if data and 'currentBlock' in data:
        blockcount = int(data['currentBlock'])
    else:
        blockcount = 0
    return blockcount


def gettransactionbyhash(hash, provider='http://127.0.0.1:8545', tojson=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    data = web3.eth.getTransaction(hash)
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)
    return data


def gettransactionreceiptbyhash(hash, provider='http://127.0.0.1:8545', tojson=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    #hash = int('0xBF75B4EeF9F8948eDF07460045aa990eFF6044a30x2e64cec1', 16)
    #print(hash)
    #print(utils.encode_hex(hash))
    #hash = utils.encode_hex(hash)
    #hash = '0x' + utils.encode_hex(hash)
    #print(hex(hash))
    #hash = '0xb01df22b392d9c5dd5a708f4ec91f952a4936f7c7e13c0fc1a685047e26e23f2'
    #print(hash)
    if isinstance(hash, int):
        hash = hex(hash)
    data = web3.eth.getTransactionReceipt(hash)
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)
    return data

# https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.getBlockTransactionCount
# blockid can be block number or block hash
def getblocktransactioncount(blockid, provider='http://127.0.0.1:8545', tojson=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    data = web3.eth.getBlockTransactionCount(blockid)
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)
    return data


# https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.getTransactionByBlock
def gettransactionfromblock(blocknumber=0, txindex=0, provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    data = web3.eth.getTransactionByBlock(blocknumber, txindex)
    data = web3.toJSON(data)
    return data

# https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.waitForTransactionReceipt
def waitfortransactionreceipt(hash, provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    data = web3.eth.waitForTransactionReceipt(hash)
    return data


# find the value of a key in the mapping
# https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/
# https://ethereum.stackexchange.com/questions/49873/how-to-derive-the-storage-key-of-mapping-to-an-account
# i = position (slot)
# k = the key to the mapping
# suitable for mapping or arrays
# in mapping, the slot is empty. in array, the slot shows the array size
def getstorageatindex(contractaddress, i, k, provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    pos = str(remove_0x_prefix(i)).rjust(64, '0')
    key = remove_0x_prefix(k).rjust(64, '0').lower()
    storage_key = to_hex(web3.sha3(hexstr=key + pos))
    return storage_key, to_int(web3.eth.getStorageAt(contractaddress, storage_key))


def getstoragepos(i, k):
    #pos = str(i).rjust(64, '0')
    pos = getstoragekey(i, k)
    #print(pos)
    key = str(remove_0x_prefix(pos)).rjust(64, '0').lower()
    storage_key = to_hex(Web3auto.sha3(hexstr=key))
    return storage_key
    #return getstoragekey(i,2)



# https://ethereum.stackexchange.com/questions/49873/how-to-derive-the-storage-key-of-mapping-to-an-account
def getstoragekey(i, k):
    if isinstance(k, int):
        k = hex(k)
    k = str(k)
    pos = str(i).rjust(64, '0')
    key = remove_0x_prefix(k).rjust(64, '0').lower()
    storage_key = to_hex(Web3auto.sha3(hexstr=key + pos))
    return storage_key


# https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.getStorageAt
# blockid can be block number or block hash
# positions should be a list, but the example uses an integer
# this is suitable for variables
def getstorageat(account, positions, provider='http://127.0.0.1:8545', tojson=False, poa=False):
    if isinstance(account, int):
        account = hex(account)
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    data = web3.eth.getStorageAt(account, positions)
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)
    return data


# state proof, to be used with block.stateRoot
def getproof(account, positions, blockid, provider='http://127.0.0.1:8545', tojson=False, poa=False):
    if isinstance(account, int):
        account = hex(account)
    #print(account)
    #print(positions)
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    if poa:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    data = web3.eth.getProof(account, positions, blockid)
    #print(data)
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)
    return data


###################################### GENERAL FUNCTIONS ########################################################

# @dev createnewkey will create an Ethereum keypair. It returns address and private key respectively
# @param password is the password to generate the keypair
# @param address is the first output
# @param privateKey is the second output
"""
# keypair generation
addr,privkey = createnewkeylocal('abc')
print(addr,privkey)
"""
def createnewkeylocal(password, provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    acct = web3.eth.account.create(password)
    return acct.address, acct.privateKey.hex()


######################################### TRANSACTION AND FUNCTION CALL ########################################################


# @dev gasprice computes the gas price
# @dev manually determined
# @dev for testing, set gasprice to 0
# @Todo create gas strategy https://web3py.readthedocs.io/en/stable/gas_price.html
# the below function returns 0. Need further work
def gasprice(provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    price = web3.eth.generateGasPrice()
    manualprice = 0
    if price is None:
        price = web3.toWei(manualprice, 'gwei')
    #return web3.toWei(0, 'gwei')
    return price


# @dev nonce computes the nonce or the number of transactions created by the address
# including pending transactions
def nonce(address, provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    return web3.eth.getTransactionCount(address, 'pending')


# hosted accounts
# https://web3py.readthedocs.io/en/stable/web3.eth.account.html
def getaccounts(provider='http://127.0.0.1:8545'):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    return web3.eth.accounts


# @dev callfunc is a common function to call a contract's function
# @dev can only be used to call functions without arguments
# @param cAddress is contract address
# @param cAbi is contract ABI
def callfunctionsc(provider, contractaddress, contractabi, functionname):
    # instantiate web3
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    myContract = web3.eth.contract(address=contractaddress, abi=contractabi)
    functionToCall = myContract.functions[functionname]
    functionResult = functionToCall().call()
    return functionResult


# @dev callfunc is a common function to call a contract's function
# @dev can be used to call functions without arguments
# @param cAddress is contract address
# @param cAbi is contract ABI
# https://web3py.readthedocs.io/en/stable/contracts.html
# **functionargs should be keyword arguments (dictionary), example: args = {'blockHash': 1}
def callfunctionsckwargs(provider, contractaddress, contractabi, functionname, **functionargs):
    # instantiate web3
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    myContract = web3.eth.contract(address=contractaddress, abi=contractabi)
    functionToCall = myContract.functions[functionname]
    functionResult = functionToCall(**functionargs).call()
    return functionResult


# @dev callfunc is a common function to call a contract's function
# @dev can be used to call functions without arguments
# @param cAddress is contract address
# @param cAbi is contract ABI
# https://web3py.readthedocs.io/en/stable/contracts.html
# **functionargs should be positional arguments, example: args = [1]
def callfunctionscpargs(provider, contractaddress, contractabi, functionname, *functionargs):
    # instantiate web3
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    myContract = web3.eth.contract(address=contractaddress, abi=contractabi)
    functionToCall = myContract.functions[functionname]
    functionResult = functionToCall(*functionargs).call()
    return functionResult


# generate raw transaction locally
# https://ethereum.stackexchange.com/questions/77675/why-does-web3py-need-provider-to-initialize-contract
# or, use w3 by importing it: from web3.auto import w3 # https://web3py.readthedocs.io/en/stable/filters.html#filtering
def localrawtransaction(chainid, gas, gasprice, nonce, accountprivatekey, contractaddress, contractabi, functionname, **functionargs):
    # does not specify provider
    web3 = Web3()
    mycontract = web3.eth.contract(address=str(contractaddress), abi=contractabi)
    myfunction = mycontract.functions[functionname](**functionargs)

    detailTx = {'chainId': chainid, 'gas': gas, 'gasPrice': gasprice,
                'nonce': nonce, }
    unsignedTx = myfunction.buildTransaction(detailTx)
    signedTx = web3.eth.account.signTransaction(unsignedTx, private_key=accountprivatekey)
    return signedTx.rawTransaction


def executefunctionsc(receiptmode, provider, accountaddress, accountprivatekey, contractaddress, contractabi, functionname, **functionargs):
    # instantiate web3
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    mycontract = web3.eth.contract(address=str(contractaddress), abi=contractabi)

    # modify this part on on different functions
    myfunction = mycontract.functions[functionname](**functionargs)
    # gas estimation
    # https://web3py.readthedocs.io/en/stable/examples.html#working-with-contracts

    # @TODO fix this gas estimation function
    # issues with estimateGas that requires more than 50k gas  https://github.com/INFURA/infura/issues/108
    # gas depends on the node https://github.com/ethereum/web3.py/issues/845
    #gasestimate = myfunction.estimateGas()
    gasestimate = 1000000
    gasestimate = gasestimate + 9000000
    if accountaddress == '':
        try:
            #print("wew")
            web3.eth.defaultAccount = web3.eth.accounts[0]
            #print(myfunction.transact())
            tx_hash = myfunction.transact()
            #print(tx_hash)
            if receiptmode:
                receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                # dictionary
                '''
                AttributeDict({'transactionHash': HexBytes('0x8220a034e0b73f0c6e9fa9f9d7ebb355d9c08985507fe72e3ba4167a4d9b764f'), 'transactionIndex': 0, 'blockHash': HexBytes('0xd51eacaf5a00bc424443f79a6ae59ca02da35a13180beead09f3f6e38ebc6a71'), 'blockNumber': 3, 'from': '0x0da2Afba0e07A1E22027A62Db4423B59e6ac8D58', 'to': '0x861a9cfC5586f86F33B2C0A4C87eB4050F728979', 'gasUsed': 21484, 'cumulativeGasUsed': 21484, 'contractAddress': None, 'logs': [], 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
    
                '''
                return to_hex(receipt.transactionHash)
            else:
                return to_hex(tx_hash)
        except:
            return False
    else:
        chainid = getchainid(provider)
        detailTx = {'chainId': chainid, 'gas': gasestimate, 'gasPrice': gasprice(provider), 'nonce': nonce(accountaddress, provider), }
        unsignedTx = myfunction.buildTransaction(detailTx)
        #print(unsignedTx)
        signedTx = web3.eth.account.signTransaction(unsignedTx, private_key=accountprivatekey)

        try:
            tx_hash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
            if receiptmode:
                receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                #print(receipt)
                # AttributeDict({'blockHash': HexBytes('0x497f2e059e5773b2b6a527935fe05eebdc8d0f70ae811468ac83ca34ffef82e1'), 'blockNumber': 8167, 'contractAddress': None, 'cumulativeGasUsed': 26348, 'from': '0x1283A1E9f092a6c8554ca7F825AE14CC47043cB9', 'gasUsed': 26348, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 0, 'to': '0x9c742A6E8f0935C3bf2B3d3f4Ff9f5bc1d249EB4', 'transactionHash': HexBytes('0xe0e6a7b371eea27f0d605739b0f962384270c7c38200db8bc0b724fc0a97e46b'), 'transactionIndex': 0})
                if (receipt.status == 1):
                    return to_hex(receipt.transactionHash)
                else:
                    return False
            else:
                return to_hex(tx_hash)
        except:
            return False


###################################### ABI ########################################################

# read ABI from file
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
def getabi(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data['abi']


###################################### FILTER ########################################################

# still returns nothing
def filternewblocks(provider):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    filter = web3.eth.filter('latest')
    print(filter.get_new_entries())
    return filter.get_new_entries()

'''
Example result:
[AttributeDict({'args': AttributeDict({'num': 1}), 'event': 'StoreNum', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xda9dc17dce7ae3f6f7375f54c7051745428653ee15fdbe6e752888a3229f52a8'), 'address': '0xda559eAE6F6A06A9202DE38c08b8508FC069493d', 'blockHash': HexBytes('0xb7756141a656c758585ae51ee01000a440bb2db2f5210ddfda049b9d47124f5d'), 'blockNumber': 1800})]
[{'args': {'num': 1}, 'event': 'StoreNum', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': '0xda9dc17dce7ae3f6f7375f54c7051745428653ee15fdbe6e752888a3229f52a8', 'address': '0xda559eAE6F6A06A9202DE38c08b8508FC069493d', 'blockHash': '0xb7756141a656c758585ae51ee01000a440bb2db2f5210ddfda049b9d47124f5d', 'blockNumber': 1800}, {'args': {'num': 2}, 'event': 'StoreNum', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': '0x1cb430206f29b2c418001ead516eaeeb146129dee9a5612077747c90abdbbc11', 'address': '0xda559eAE6F6A06A9202DE38c08b8508FC069493d', 'blockHash': '0x045ad7df6c5a74f7710dea71732a0b14026f516a39d4f2ddbfa26428484e8257', 'blockNumber': 1823}]

'''
def eventfilter(provider, contractaddress, contractabi, eventname, firstblock, lastblock, mode=['all', 'new'], tojson=False):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    myContract = web3.eth.contract(address=contractaddress, abi=contractabi)
    myEvent = myContract.events[eventname]
    myFilter = myEvent.createFilter(fromBlock=firstblock, toBlock=lastblock)
    #myFilter = myContract.eventFilter(eventname, {'fromBlock': 0, 'toBlock': 'latest'})
    if mode == 'all':
        data = myFilter.get_all_entries()
    elif mode == 'new':
        data = myFilter.get_new_entries()
    if tojson:
        data = web3.toJSON(data)
        data = json.loads(data)
    return data

# @dev eventstampdutypayment check the event eStampDutyPayment
# @dev based on payCode
# @dev DO NOT USE. THIS WILL CRASH GANACHE
# @TODO: fix this!
def eventfilterx(provider, contractaddress, contractabi, **kwargs):
    web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
    myContract = web3.eth.contract(address=contractaddress, abi=contractabi)
    #myFilter = myContract.events.eStampDutyPayment.createFilter(fromBlock='latest', argument_filters={'payer':payer})
    #myFilter = myContract.events.createFilter(fromBlock='0', toBlock='latest', argument_filters=**kwargs)
    #event_signature_hash = web3.sha3(text="eStampDutyPayment(bytes32, string, bytes32, string, address)").hex()
    #event_filter = web3.eth.filter({
    #    "address": contractAddress,
    #    "topics": [event_signature_hash],
    #})
    #return event_filter.get_all_entries()
    ##return myFilter.get_all_entries()
    #myFilter = myContract.eventFilter('eStampDutyPayment', {'fromBlock':0, 'toBlock':'latest'})
    #eventList = myFilter.get_all_entries()
    #return eventList

######################################################


def main():
    fire.Fire()


if __name__ == "__main__":
    main()

