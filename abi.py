'''
sonicskye@2020

Load JSON ABI from files
'''

import os
import json
import fire

#_PATH = os.path.dirname(os.path.realpath(__file__)) + "/db/" + dbname
ABI_PATH = os.path.dirname(os.path.realpath(__file__)) + "/abi/"

contractaddress = "0xbfaC3e6913306C8ED630079832C17C97bCEDB8a3"
btcrelayabifilename = 'BTCRelay.json'


# read ABI from file
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
def getabi(filename):
    with open(ABI_PATH + filename) as json_file:
        data = json.load(json_file)
    return data['abi']


def getabibtcrelay():
    return getabi(btcrelayabifilename)


###################################### MAIN ########################################################


def main():
    fire.Fire()


if __name__ == "__main__":
    main()