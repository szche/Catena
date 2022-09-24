import requests
import typing
import hashlib
import json

from merkle import MerkleClient

class Catena(object):
    def __init__(self, genesis_tx):
        self.server_url = "http://localhost:5000"
        self.genesis_tx = genesis_tx
        self.statements = []

    def verifyTx(self, tx, chainTip):
        print(tx)

        # Verify that tx is confirmed
        assert tx['status']['confirmed'] == True, 'Tx is not confirmed'

        # Verify that tx is confirmed with at least 6 confirmations
        assert chainTip - tx['status']['block_height'] >=6, 'Tx has less than 6 confirmations'
        
        pass

    def verifyBlock(self, block):
        pass

    def getProofFromServer(self, file_hash: str):
        response = requests.get(f'{self.server_url}/verify?file={file_hash}')
        #if response.status_code != 200 or response.header['Content-Type'] != 'application/json':
        #    return False
        return json.loads(response.text)

    def verifyStatement(self, OP_RETURNs_api, statement):
        if statement in OP_RETURNs_api:
            return True
        return False



catena = Catena("asdasd")
proof = catena.getProofFromServer("asdasd")
merkle_client = MerkleClient()
print(merkle_client.count_root("hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni", proof))
    
