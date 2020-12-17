# btcrelay-ui
Python-based Interface to communicate with BTCRelay Ethereum smart contract

## Requirements
- [BTCRelay-sol](https://github.com/sonicskye/btcrelay-sol)
- Python3
- virtualenv
- all packages in requirements.txt

## How to 
- Deploy btcrelay contract
- store the address in vars.py
- assume the node address is http://127.0.0.1:8545  
- initialise the relay. specifically for genesis block
```
python fetchd.py relayinitial 'http://127.0.0.1:8545'
```
- relay blocks. To relay block 1 to 100, the command is
```
python fetchd.py relayblockheaders 'http://127.0.0.1:8545' 0 100
```