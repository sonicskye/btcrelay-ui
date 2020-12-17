import os
from ethrpcops import getabi

# ganache GUI as the provider/HTTP
#provider = "http://127.0.0.1:7545"

# ganache-cli as the provider/HTTP
provider = "http://127.0.0.1:7545"

# truffle develop as the provider/HTTP
#provider = "http://127.0.0.1:9545"

# geth as the provider/IPC
# WARNING: Proof-of-Authority requires extra work, currently not supported
#provider = "~/Ethereum/geth/networkid456/geth.ipc"

# contractAddress is the address of the contract after deployed to the network
# modify according to your own contract address
BTCRelayContractAddress = '0x9BDb328052213228A92e4498F16090E821feA04E'
HelperContractAddress = '0xdE898EA40c485CA4609Ad0F969A7819C27d7F934'

# ABI file
BTCRelayContractABI = getabi(os.path.dirname(os.path.realpath(__file__)) + '/abi/BTCRelay.json')
HelperContractABI = getabi(os.path.dirname(os.path.realpath(__file__)) + '/abi/Helper.json')

# my own API
blockchain_com_api_key = ''