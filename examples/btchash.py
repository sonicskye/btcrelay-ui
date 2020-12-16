# https://bitcoin.stackexchange.com/questions/67791/calculate-hash-of-block-header

from hashlib import sha256
import hashlib
import binascii

# https://www.blockchain.com/btc/block/0000000000000000000635bda771916ca727db53fea5441508f7161386e066be
# https://blockchain.info/block/0000000000000000000635bda771916ca727db53fea5441508f7161386e066be?format=hex

header = binascii.unhexlify("0000002066720b99e07d284bd4fe67ff8c49a5db1dd8514fcdab610000000000000000007829844f4c3a41a537b3131ca992643eaa9d093b2383e4cdc060ad7dc548118751eb505ac1910018de19b302")
print(binascii.hexlify(sha256(sha256(header).digest()).digest()[::-1]).decode())