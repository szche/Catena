import typing
import hashlib
import sys

from bitcoinapi import BitcoinAPI
from catena import Catena
from merkle import MerkleClient
from signtool import SignTool
from cert_lookup import CertLookup

GENESIS_TX = '13c7ef106183ced5a2119b2a46670988dd456c82cc3c87318d8e8c5cba2c3ac1'


def check_update(btc_api, catena):
    print("This is a mock-up of a calculator app that desperatly needs secure update!")
    print("Thankfully it's using the Catena protocol!")
    print("Genesis tx:", GENESIS_TX)


    print("Veryfing that this tx is included in the chain...") 

    print(btc_api.blockTipHash)
    print(btc_api.blockTipHeight)

    # Fetching info about genesis TX from the API
    tx_info = btc_api.tx(GENESIS_TX)
    current_block_height = btc_api.blockTipHeight

    #catena.verifyTx(tx_info, current_block_height)
    


def calculator(btc_api, catena, merkle_client, signtool, file_path):
    
    # get hash from the file_path
    file_hash = signtool.get_hash_of_file(file_path)

    #get proof from the server
    proof = catena.getProofFromServer(file_hash)

    # count root from file hash and proof
    #merkle_root_of_file = merkle_client.count_root(file_hash, proof)
    merkle_root_of_file = merkle_client.count_root("hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni", proof)
    # get BTC address from cert
    btc_address = signtool.extract_btc_address(file_path)
    op_returns = btc_api.get_OPs(btc_address)

    #print(op_returns)
    decision = catena.verifyStatement(op_returns, merkle_root_of_file)
    #print(decision)
    if not decision:
        sys.exit("Sygnatura pliku nie została dodana do łańcucha bloków")

    # TODO
    # lekki refactor i spojrzenie czy blok z danym returnem ma STATUS ora 6> blocków
    # rozmkinka czy trzeba jakoś sprawdzać ciągłość transakcji według genesis_tx
    # TODO check_update - może to jakoś asynchronicznie pobierać

if __name__ == "__main__":
    print("Running update checker on start-up...")

    file_path = sys.argv[1]
    # all classes
    btc_api = BitcoinAPI()
    catena = Catena(GENESIS_TX)
    merkle_client = MerkleClient()
    signtool = SignTool()

    check_update(btc_api, catena)
    calculator(btc_api, catena, merkle_client, signtool, file_path)

    




