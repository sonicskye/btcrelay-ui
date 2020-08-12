'''
sonicskye@2020


'''

from web3 import Web3
from vars import provider
from abi import contractaddress, getabibtcrelay
import fire

web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))

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
def createnewkeylocal(password):
    acct = web3.eth.account.create(password)
    return acct.address, acct.privateKey.hex()


# @dev gasprice computes the gas price
# @dev manually determined
# @dev for testing, set gasprice to 0
# @Todo create gas strategy https://web3py.readthedocs.io/en/stable/gas_price.html
def gasprice():
    return web3.toWei(0, 'gwei')


# @dev nonce computes the nonce or the number of transactions created by the address
def nonce(address):
    return web3.eth.getTransactionCount(address)


# hosted accounts
# https://web3py.readthedocs.io/en/stable/web3.eth.account.html
def accounts():
    return web3.eth.accounts


# @dev callfunc is a common function to call a contract's function
# @dev can only be used to call functions without arguments
# @param cAddress is contract address
# @param cAbi is contract ABI
def callfunc(cAddress, cAbi, functionName):
    myContract = web3.eth.contract(address=cAddress, abi=cAbi)
    functionToCall = myContract.functions[functionName]
    functionResult = functionToCall().call()
    return functionResult


###################################### FUNCTION CALLS ########################################################

# @dev setinitialparent sets an initial parent
# @dev returns the transaction ID
# @param bytes blockHeaderBytes;
# @param uint32 blockHeight;
# @param uint256 chainWork;
# @param uint256 lastDiffAdjustmentTime;
def setinitialparent(blockHeaderBytes, blockHeight, chainWork, lastDiffAdjustmentTime, address='', privateKey=''):
    # gas cost based on trial on Remix is
    # gas cost based on trial on Ganache is  and
    gas = 30000000
    myContract = web3.eth.contract(address=contractaddress, abi=getabibtcrelay())
    detailTx = {'chainId': 1, 'gas': gas, 'gasPrice': gasprice(), 'nonce': nonce(address), }
    unsignedTx = myContract.functions.setInitialParent(blockHeaderBytes, blockHeight, chainWork,
                                                       lastDiffAdjustmentTime).buildTransaction(detailTx)
    if address == '':
        try:
            txid = web3.eth.sendTransaction(unsignedTx)
            return "Transaction ID: " + txid
        except:
            return "transaction failed"
    else:
        signedTx = web3.eth.account.signTransaction(unsignedTx, private_key=privateKey)
        # send the transaction
        #web3.eth.sendRawTransaction(signedTx.rawTransaction)
        try:
            web3.eth.sendRawTransaction(signedTx.rawTransaction)
            return "Transaction ID: " + web3.toHex(web3.sha3(signedTx.rawTransaction))
        except:
            return "transaction failed"


###################################### MAIN ########################################################


def main():
    fire.Fire()


if __name__ == "__main__":
    main()