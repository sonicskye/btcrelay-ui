'''
http://pythonfiddle.com/merkle-root-bitcoin/
was originally in Python2

Convert to Python3
https://stackoverflow.com/questions/54790293/python-3-print-result-of-function-giving-error
'''

import hashlib
import binascii
import codecs
import fire


# Hash pairs of items recursively until a single value is obtained
def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList) - 1, 2):
        newHashList.append(hash2(hashList[i], hashList[i + 1]))
    if len(hashList) % 2 == 1:  # odd, hash last item twice
        newHashList.append(hash2(hashList[-1], hashList[-1]))
    #print(newHashList)
    return merkle(newHashList)


# Hash pairs of items recursively until a single value is obtained
# compute merkle root hash and depth
def merkledepth(hashList, depth=0):
    if len(hashList) == 1:
        return hashList[0], depth
    newHashList = []
    depth += 1
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList) - 1, 2):
        newHashList.append(hash2(hashList[i], hashList[i + 1]))
    if len(hashList) % 2 == 1:  # odd, hash last item twice
        newHashList.append(hash2(hashList[-1], hashList[-1]))
    #print(newHashList)
    return merkledepth(newHashList, depth)


def depth(leafcount=1):
    enough = False
    height = 0
    if leafcount <= 0:
        return height
    while not enough:
        height+= 1
        capacity = 2**height
        if leafcount <= capacity:
            enough = True
    return height


# https://medium.com/coinmonks/how-to-manually-verify-the-merkle-root-of-a-bitcoin-block-command-line-7881397d4db1
def merkleproof(hashList, hash, proof=[]):
    if len(hashList) == 1:
        return proof
    newHashList = []
    hash1 = hash
    #print(hashList)
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList) - 1, 2):
        if hashList[i] == hash1 or hashList[i+1] == hash1:
            if hashList[i] == hash1:
                proof.append(hashList[i+1])
                #print('left ' + hashList[i+1])
            elif hashList[i+1] == hash1:
                proof.append(hashList[i])
                #print('right ' + hashList[i])
            hash1 = hash2(hashList[i], hashList[i + 1])
            #print(hash1)
            #proof.append(hash1)
        #hash1 = hash2(hashList[i], hashList[i + 1])
        newHashList.append(hash2(hashList[i], hashList[i + 1]))
    if len(hashList) % 2 == 1:  # odd, hash last item twice
        if hashList[-1] == hash1:
            proof.append(hashList[-1])
            hash1 = hash2(hashList[-1], hashList[-1])
        newHashList.append(hash2(hashList[-1], hashList[-1]))
    return merkleproof(newHashList, hash1, proof)


# https://www.geeksforgeeks.org/python-program-to-covert-decimal-to-binary-number/
def decimaltobinary(n):
    return bin(n).replace("0b", "")


# https://bitcoin.stackexchange.com/questions/69018/merkle-root-and-merkle-proofs
def prove(merkleroot='', merkleproof=[], txid='', idx=0, depth=1):
    if merkleroot == '':
        return False
    if len(merkleproof) == 0:
        return False
    if depth < 1:
        return False
    if depth == 1:
        if merkleroot == txid:
            return True
        else:
            return False
    total = 2**depth + idx
    binnum = str(decimaltobinary(total)[1:][::-1])
    hash = txid
    j = 0
    for i in range(0, len(str(binnum))):
        # if 0 then left, otherwise right
        if binnum[i] == '0':
            hash = hash2(hash, merkleproof[i])
        elif binnum[i] == '1':
            hash = hash2(merkleproof[i], hash)
        j += 1
    if hash == merkleroot:
        return True
    else:
        return False


def hash2(a, b):
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    a1 = binascii.unhexlify(a)[::-1]
    b1 = binascii.unhexlify(b)[::-1]
    # double sha256 of a1+b1
    h = hashlib.sha256(hashlib.sha256(a1+b1).digest()).digest()
    return binascii.hexlify(h[::-1]).decode() # add .decode() here if you want str instead of bytes


def sample():

    # https://blockexplorer.com/rawblock/000000000000030de89e7729d5785c4730839b6e16ea9fb686a54818d3860a8d
    txHashes = [
        "338bbd00b893c384eb2b11e70f3875447297c5f20815499e787867df4538e48d",
        "1ad1138c6064dd17d0a4d12016d629c18f15fc9d1472412945f9c91a696689c7",
        "c77834d14d66729014b06fcf45c5f82af4bdd9d816e787f01bfa525cfa147014",
        "bb3d83398d7517fe643b2421d795e73c342b6a478ef53acdaab35dbdffbbcdb5",
        "38d563caf0e9ed103515cab09e40e49da0ccb8c0765ce304f9556e5bc62e8ff5",
        "8fc0507359d0122fa14b5887034d857bd69c8bc0e74c8dd428c2fc098595c285",
        "9db9fe6d011c1c7e997418aeec78ccb659648cfc915b2ff1154cabb41359ac70",
        "3c72fdb7e38e4437faa9e5789df6b51505de014b062361ef47578244d5025628"
    ]

    '''
    txHashes = [
        "e2d23adf5c86b1266a6abb9a471eaa05bf233dc66245e36a82bb14392fb36c47",
        "13f0f97659ccb96f0f6abd4cda25894463dec0cf3deb626acfc60d506bfd3650"
    ]
    '''
    #print(merkle(txHashes))

    #print(merkledepth(txHashes))

    # the txhash to get the merkle proof
    hash = "3c72fdb7e38e4437faa9e5789df6b51505de014b062361ef47578244d5025628"
    idx = txHashes.index(hash)
    print(merkleproof(txHashes, hash))
    #print(merkle(txHashes))


    merkleroot=merkle(txHashes)
    merkleproofdata=merkleproof(txHashes, hash)
    txid=hash
    depthdata=depth(len(txHashes))
    print(prove(merkleroot, merkleproofdata, txid, idx, depthdata))

######################################################


def main():
    fire.Fire()


if __name__ == "__main__":
    main()