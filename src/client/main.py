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
    print_handler("info", "This is a mock-up of a calculator app that desperatly needs secure update!")
    print_handler("info", "Thankfully it's using the Catena protocol!")
    print_handler("info", "Genesis tx:" + GENESIS_TX)


    print_handler("info", "Veryfing that this tx is included in the chain...") 

    print_handler("info", "Hash ostatniego bloku: " + str(btc_api.blockTipHash))
    print_handler("info", "Obecna wysokość bloku: " + str(btc_api.blockTipHeight))

    # Fetching info about genesis TX from the API
    tx_info = btc_api.tx(GENESIS_TX)
    current_block_height = btc_api.blockTipHeight

    #catena.verifyTx(tx_info, current_block_height)
    


def calculator(btc_api, catena, merkle_client, signtool, cert_lookup, file_path):
    
    # get hash from the file_path
    print_handler("info", "Liczę skrót z pliku")
    file_hash = signtool.get_hash_of_file(file_path)
    if file_hash in ["", None]:
        print_handler("warning", "Błąd przy wyliczeniu skrótu z pliku")

    #get proof from the server
    print_handler("info", "Generuje zapytanie do serwera Cateny")
    proof = catena.getProofFromServer(file_hash)
    if proof in [None, ""]:
        print_handler("warning", "Pobrano niepoprawny proof z serwera")
    print_handler("info", "Proof " + str(proof))

    # count root from file hash and proof
    print_handler("info", "Liczę korzeń drzewa Merkle")
    merkle_root_of_file = merkle_client.count_root(file_hash, proof)
    #merkle_root_of_file = merkle_client.count_root("hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni", proof)

    # get signature_info
    signature_info = signtool.verify(file_path)
    if signature_info["status"] != "Valid":
        print_handler("warning", "Nie udało się odczytać danych certyfikatu")
        sys.exit()
    
    # get thumbprint from signature_info
    thumbprint = signature_info["thumbprint"]
    if thumbprint in [None, ""]:
        print_handler("warning", "Nie udało się odczytać sygnatury")
    # verify cert
    if cert_lookup.find_by_thumbprint(thumbprint) == False:
        print_handler("warning", "Podany certyfikat nie jest zaimportowany")
        sys.exit()

    # get BTC address from cert
    print_handler("info", "Pobieram adres portfela z pliku")
    btc_address = signtool.extract_btc_address(file_path)
    if btc_address in [None, ""]:
        print_handler("warning", "Nie udało się pobrać adresu portfela z pliku")
    # get all OP_RETURNS from given address
    print_handler("info", "Pobieram OP_RETURNS z transakcji")
    op_returns = btc_api.get_OPs(btc_address)

    # get current block height
    chainTip = btc_api.blockTipHeight
    # verify is file hash is in confirmed block/transaction
    print_handler("info", "Weryfikuję czy hash pliku jest w sieci Bitcoin")
    decision = catena.verifyStatement(op_returns, merkle_root_of_file, chainTip)
    print_handler("info", decision)
    if decision:
        print_handler("success", "Plik znajduje się w łańcuchu bloków")
    else:
        print_handler("warning", "Plik nie znajduje się w łańcuchu bloków")

def print_handler(log_type, text):
    if log_type == "info":
        prefix = "[INFO]"
    elif log_type == "warning":
        prefix = "\033[2;31;43m [WARNING] \033[0;0m"
    elif log_type == "success":
        prefix = "[SUCCESS]"
    else:
        prefix = "[...]"

    print(prefix + " Catena Client -> " + str(text)) 

if __name__ == "__main__":
    print_handler("info", "Running update checker on start-up...")

    file_path = sys.argv[1]
    # all classes
    btc_api = BitcoinAPI()
    catena = Catena(GENESIS_TX)
    merkle_client = MerkleClient()
    signtool = SignTool()
    cert_lookup = CertLookup()

    check_update(btc_api, catena)
    calculator(btc_api, catena, merkle_client, signtool, cert_lookup, file_path)
