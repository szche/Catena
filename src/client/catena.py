import requests
import typing
import hashlib
import json
import sys

from merkle import MerkleClient

class Catena(object):
    def __init__(self, genesis_tx):
        self.server_url = "http://localhost:5000"
        self.server_url_public = "http://54.167.43.197:5000"
        self.genesis_tx = genesis_tx
        self.statements = []

    def verifyTx(self, tx, chainTip):

        # Verify that tx is confirmed
        if tx['tx_status']['confirmed'] != True:
            sys.exit('[WARNING] Catena Client --> Tx is not confirmed')
        #assert tx['tx_status']['confirmed'] == True, 'Tx is not confirmed'

        # Verify that tx is confirmed with at least 6 confirmations
        if  chainTip - tx['tx_status']['block_height'] <=6:
            sys.exit('[WARNING] Catena Client --> Tx has less than 6 confirmations')
        #assert chainTip - tx['tx_status']['block_height'] >=6, 'Tx has less than 6 confirmations'

        pass

    def verifyBlock(self, block):
        pass

    def getProofFromServer(self, file_hash: str):
        response = requests.get(f'{self.server_url_public}/verify?file={file_hash}')
        if response.status_code != 200:
            return False
        return json.loads(response.text)

    def verifyStatement(self, OP_RETURNs_api, statement, chainTip):
        for one in OP_RETURNs_api:
            if one["op_return"] == statement:
                self.verifyTx(one, chainTip)
                return True
        return False




#catena = Catena("asdasd")
#proof = catena.getProofFromServer("asdasd")
#merkle_client = MerkleClient()
#rint(merkle_client.count_root("hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni", proof))
    
