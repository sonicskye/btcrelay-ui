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




def get_hash_by_height(height):
    url = 'https://blockchain.info/block-height/'+str(height)+'?format=json'
    # https://stackoverflow.com/a/23565355
    response = requests.get(url)
    jsonurl = response.content
    text = json.loads(jsonurl)
    return text['blocks'][0]['hash']


# format can be json or hex
def get_block_header_by_hash(hash, format='json'):
    url = 'https://blockchain.info/rawblock/' + str(hash) + '?format=' + str(format)
    # https://stackoverflow.com/a/23565355
    response = requests.get(url)
    if format == 'hex':
        return response.content
    else:
        jsonurl = response.content
        text = json.loads(jsonurl)
        return text


# format can be json or hex
def get_block_by_hash(hash, format='json'):
    url = 'https://blockchain.info/block/' + str(hash) + '?format=' + str(format)
    # https://stackoverflow.com/a/23565355
    response = requests.get(url)
    if format == 'hex':
        return response.content
    else:
        jsonurl = response.content
        text = json.loads(jsonurl)
        return text


# format can be json or hex
def get_block_header_by_height(height, format='json'):
    hash = get_hash_by_height(height)
    blockheader = get_block_header_by_hash(hash, format)
    return blockheader


# format can be json or hex
def get_block_by_height(height, format='json'):
    hash = get_hash_by_height(height)
    block = get_block_by_hash(hash, format)
    return block


# get the first 80 bytes of the rawblock
def extract_rawblockheader_from_rawblock(rawblock):
    rawblockheader = rawblock[0:160]
    return rawblockheader


# serializing block header data
# https://en.bitcoin.it/wiki/Block_hashing_algorithm
# version 4 bytes
# hashPrevBlock 32 bytes
# hashMerkleRoot 32 bytes
# time 4 bytes
# bits 4 bytes
# nonce 4 bytes
def serialize_header(version, hash_prev_block, hash_merkle_root, time, bits, nonce):
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    #ver_format = binascii.unhexlify(version)[::-1]
    pass


def test():
    #data = '00000020aa7483d896e00427196905408d75d5aa05c7b584e584470000000000000000003268f5aa4821f80eacc7b8ff77eebee70b7d1262b46adbf579af2464029bae8f68cd845af8e96117b2d95c65'
    rawblock = get_block_by_height(1, 'hex')
    rawblockheader = extract_rawblockheader_from_rawblock(rawblock)
    print(header_hash(rawblockheader))



######################################################


def main():
    fire.Fire()


if __name__ == "__main__":
    main()