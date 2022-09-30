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
    print_handler("This is a mock-up of a calculator app that desperatly needs secure update!")
    print_handler("Thankfully it's using the Catena protocol!")
    print_handler("Genesis tx:" + GENESIS_TX)


    print_handler("Veryfing that this tx is included in the chain...") 

    print_handler("Hash ostatniego bloku: " + str(btc_api.blockTipHash))
    print_handler("Obecna wysokość bloku: " + str(btc_api.blockTipHeight))

    # Fetching info about genesis TX from the API
    tx_info = btc_api.tx(GENESIS_TX)
    current_block_height = btc_api.blockTipHeight

    #catena.verifyTx(tx_info, current_block_height)
    


def calculator(btc_api, catena, merkle_client, signtool, file_path):
    
    # get hash from the file_path
    print_handler("Liczę hash z pliku")
    file_hash = signtool.get_hash_of_file(file_path)

    #get proof from the server
    print_handler("Generuje zapytanie do serwera Cateny")
    proof = catena.getProofFromServer(file_hash)
    print_handler("Proof " + str(proof))

    # count root from file hash and proof
    print_handler("Liczę korzeń drzewa Merkle")
    merkle_root_of_file = merkle_client.count_root(file_hash, proof)
    #merkle_root_of_file = merkle_client.count_root("hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni", proof)

    # get BTC address from cert
    print_handler("Pobieram adres portfela z pliku")
    btc_address = signtool.extract_btc_address(file_path)

    # get all OP_RETURNS from given address
    print_handler("Pobieram OP_RETURNS z transakcji")
    op_returns = btc_api.get_OPs(btc_address)

    # get current block height
    chainTip = btc_api.blockTipHeight
    # verify is file hash is in confirmed block/transaction
    print_handler("Weryfikuję czy hash pliku jest w sieci Bitcoin")
    decision = catena.verifyStatement(op_returns, merkle_root_of_file, chainTip)
    print_handler(decision)
    if not decision:
        sys.exit("Sygnatura pliku nie została dodana do łańcucha bloków")

    print_handler("Plik znajduje się w łańcuchu bloków")
    return True

    # TODO
    # lekki refactor i spojrzenie czy blok z danym returnem ma STATUS ora 6> blocków
    # rozmkinka czy trzeba jakoś sprawdzać ciągłość transakcji według genesis_tx
    # TODO check_update - może to jakoś asynchronicznie pobierać

def print_handler(text):
    print("Catena Client --> " + str(text))


if __name__ == "__main__":
    print_handler("Running update checker on start-up...")

    file_path = sys.argv[1]
    # all classes
    btc_api = BitcoinAPI()
    catena = Catena(GENESIS_TX)
    merkle_client = MerkleClient()
    signtool = SignTool()

    check_update(btc_api, catena)
    calculator(btc_api, catena, merkle_client, signtool, file_path)

    




