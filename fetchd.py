"""
sonicskye@2020

Extract data from blockchain.com API
https://www.blockchain.com/api/blockchain_api
"""

import json
import requests
import fire
from btcops import header_hash
import binascii
from vars import blockchain_com_api_key as api_key, \
    BTCRelayContractAddress as contract_address, BTCRelayContractABI as contract_abi
from ethrpcops import getblocknumber, callfunctionsc, executefunctionsc, callfunctionsckwargs
from btcmerkle import merkle, merkleproof, merkledepth, prove, depth
from eth_utils import to_hex, to_bytes




def get_hash_by_height(height, key=''):
    url = 'https://blockchain.info/block-height/'+str(height)+'?format=json'
    if key != '':
        url = url + '&key='+key
    # https://stackoverflow.com/a/23565355
    #print(url)
    response = requests.get(url)
    jsonurl = response.content
    text = json.loads(jsonurl)
    return text['blocks'][0]['hash']


# format can be json or hex
def get_block_header_by_hash(hash, format='json', key=''):
    url = 'https://blockchain.info/rawblock/' + str(hash) + '?format=' + str(format)
    if key != '':
        url = url + '&key='+key
    # https://stackoverflow.com/a/23565355
    response = requests.get(url)
    if format == 'hex':
        return response.content
    else:
        jsonurl = response.content
        text = json.loads(jsonurl)
        return text


# format can be json or hex
def get_block_by_hash(hash, format='json', key=''):
    url = 'https://blockchain.info/block/' + str(hash) + '?format=' + str(format)
    if key != '':
        url = url + '&key='+key
    # https://stackoverflow.com/a/23565355
    response = requests.get(url)
    if format == 'hex':
        return response.content
    else:
        jsonurl = response.content
        text = json.loads(jsonurl)
        return text


# format can be json or hex
def get_block_header_by_height(height, format='json', key=''):
    hash = get_hash_by_height(height, key)
    blockheader = get_block_header_by_hash(hash, format, key)
    return blockheader


# format can be json or hex
def get_block_by_height(height, format='json', key=''):
    hash = get_hash_by_height(height, key)
    block = get_block_by_hash(hash, format, key)
    return block


# get the first 80 bytes of the rawblock, or 160 characters
def extract_rawblockheader_from_rawblock(rawblock):
    rawblockheader = rawblock[0:160]
    return rawblockheader


def extract_rawblockheader(height):
    #data = '00000020aa7483d896e00427196905408d75d5aa05c7b584e584470000000000000000003268f5aa4821f80eacc7b8ff77eebee70b7d1262b46adbf579af2464029bae8f68cd845af8e96117b2d95c65'
    rawblock = get_block_by_height(height, 'hex', api_key)
    rawblockheader = extract_rawblockheader_from_rawblock(rawblock)
    return rawblockheader
    #print(header_hash(rawblockheader))


def extract_txs(height):
    rawblock = get_block_by_height(height, 'json', api_key)
    txids = []
    for tx in rawblock['tx']:
        txid = tx['hash']
        txids.append(txid)
    return txids


def extract_merkleroot(height):
    rawblock = get_block_by_height(height, 'json', api_key)
    return rawblock['mrkl_root']


def genmerkleproof(height, txhash):
    txs = extract_txs(height)
    #print(txs)
    srcmerkleroot = extract_merkleroot(height)
    computedmerkleroot = merkle(txs)
    if (srcmerkleroot == computedmerkleroot):
        txidx = txs.index(txhash)
        merkleproofdata = merkleproof(txs, txhash)
        depthdata = depth(len(txs))
        if prove(computedmerkleroot, merkleproofdata, txhash, txidx, depthdata):
            return merkleproofdata
        else:
            return False
    else:
        return False


def genmerkleproof_relay(height, txhash):
    txs = extract_txs(height)
    data = []
    data.append(txhash)
    if len(txs) > 1:
        merkleproofdata = genmerkleproof(height, txhash)
        srcmerkleroot = extract_merkleroot(height)
        data.extend(merkleproofdata)
        data.append(srcmerkleroot)
    datastr = ''
    datasize = len(data)
    for d in data:
        datastr = datastr + d
    return int(datastr, 16).to_bytes(datasize * 32, byteorder='big')


def gethighestblock(provider, contractaddress, contractabi):
    functionname = 'getHighestBlock'
    return callfunctionsc(provider, contractaddress, contractabi, functionname)


def computeBlockHeaderHash(provider, contractaddress, contractabi, rawblockheader):
    functionname = 'computeBlockHeaderHash'
    functionargs = {'blockHeaderBytes': rawblockheader}
    return callfunctionsckwargs(provider, contractaddress, contractabi, functionname, **functionargs)

"""
    bytes memory blockHeaderBytes, 
    uint32 blockHeight, 
    uint256 chainWork,
    uint256 lastDiffAdjustmentTime) 
    """
def relayinitial(dstProvider):
    initialHeight = 0
    chainwork = 100010001
    lastdiffadjustmenttime = 1231006505
    poa = False
    receiptmode = False
    rawblockheader = extract_rawblockheader(initialHeight)
    blockHash = header_hash(rawblockheader)
    #print(blockHash)
    #print(to_hex(computeBlockHeaderHash(dstProvider, helper_contract_address, helper_contract_abi, int(rawblockheader, 16).to_bytes(80, byteorder='big'))))
    functionname = 'setInitialParent'
    functionargs = {'blockHeaderBytes': int(rawblockheader, 16).to_bytes(80, byteorder='big'), 'blockHeight': initialHeight, 'chainWork': chainwork,
                    'lastDiffAdjustmentTime': lastdiffadjustmenttime}
    accountaddress = ''
    accountprivatekey = ''
    tx = executefunctionsc(receiptmode, dstProvider, accountaddress, accountprivatekey, contract_address,
                           contract_abi, functionname, **functionargs)
    if tx:
        print('Block number ' + str(initialHeight) + ' (' + str(blockHash) + ') ' + ': ' + str(tx))


# single process
# blockHash and rlpHeader
def relayblockheaders(dstProvider, fromHeight=0, blockToRelay=100):
    # get the latest block on the source/blockchain B
    receiptmode = False

    # get the latest relayed block on the destination/blockchain A
    destmaxheight = gethighestblock(dstProvider, contract_address, contract_abi)
    if destmaxheight == 0:
        destmaxheight = fromHeight
    sourcemaxheight = destmaxheight + blockToRelay
    print(sourcemaxheight, destmaxheight)
    print('Relaying Blocks from ' + str(destmaxheight+1) + ' to ' + str(sourcemaxheight))

    # relay block from the latest relayed block +1 to the latest (-10) block in source blockchain
    # for demonstration, we reduce it to 3
    for i in range(destmaxheight+1, sourcemaxheight+1):
        rawblockheader = extract_rawblockheader(i)
        #print(rawblockheader)
        blockHash = header_hash(rawblockheader)
        functionname = 'submitMainChainHeader'
        #print(rawblockheader)
        #print(int(rawblockheader, 16).to_bytes(80, byteorder='big'))
        #print(to_bytes(rawblockheader))
        functionargs = {'blockHeaderBytes': int(rawblockheader, 16).to_bytes(80, byteorder='big')}
        #accountaddress = '0x2C716851591990278F3F419E0fabBa7AF2f8FE0E'
        #accountprivatekey = 'f594cf7b1b07aa6a5f5b10346b63d934c9501878bf6ca18a2d84ecf05d058918'
        accountaddress = ''
        accountprivatekey = ''
        #print(rawblockheader)
        tx = executefunctionsc(receiptmode, dstProvider, accountaddress, accountprivatekey, contract_address,
                               contract_abi, functionname, **functionargs)
        if tx:
            print('Block number ' + str(i) + ' (' + str(blockHash) + ') ' + ': ' + str(tx))
        else:
            print('Relay block ' + str(i) + ' failed.')


def verifyTx(dstProvider, height, txhash):
    receiptmode = False
    merkleproofdataformatted = genmerkleproof_relay(height, txhash)
    txs = extract_txs(height)
    txidx = txs.index(txhash)
    minconfirmation = 1
    # print(blockHash)
    # function verifxTX(bytes32 txid, uint256 txBlockHeight, uint256 txIndex, bytes memory merkleProof, uint256 confirmations) public returns(bool)
    functionname = 'verifxTX'
    functionargs = {'txid':txhash, 'txBlockHeight': height, 'txIndex':txidx, 'merkleProof':merkleproofdataformatted, 'confirmations':minconfirmation}
    accountaddress = ''
    accountprivatekey = ''
    tx = executefunctionsc(receiptmode, dstProvider, accountaddress, accountprivatekey, contract_address,
                           contract_abi, functionname, **functionargs)
    if tx:
        print('Transaction ' + txhash + ' is verified through transaction ' + ': ' + str(tx))
    else:
        print('Verification failed.')


######################################################


def main():
    fire.Fire()


if __name__ == "__main__":
    main()