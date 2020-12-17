# btcrelay-ui
Python-based Interface to communicate with BTCRelay Ethereum smart contract

## Requirements
- [BTCRelay-sol](https://github.com/sonicskye/btcrelay-sol)
- Python3
- virtualenv
- all packages in requirements.txt

## How to 
- Rename vars-sample.py to vars.py
- Get API key from blockchain.info and store it in vars.py (optional).
- Deploy btcrelay contract.
- Store the address in vars.py.
- Assume the node address is http://127.0.0.1:8545.  
- Initialise the relay. This will relay the genesis block.
```
python fetchd.py relayinitial 'http://127.0.0.1:8545'
```
- Relay blocks. To relay block 1 to 100, the command is:
```
python fetchd.py relayblockheaders 'http://127.0.0.1:8545' 0 100
```