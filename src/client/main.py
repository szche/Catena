from bitcoinapi import BitcoinAPI
from catena import Catena


GENESIS_TX = '13c7ef106183ced5a2119b2a46670988dd456c82cc3c87318d8e8c5cba2c3ac1'


def check_update():
    print("This is a mock-up of a calculator app that desperatly needs secure update!")
    print("Thankfully it's using the Catena protocol!")
    print("Genesis tx:", GENESIS_TX)

    btc_api = BitcoinAPI()
    catena = Catena(GENESIS_TX)
    print("Veryfing that this tx is included in the chain...") 

    print(btc_api.blockTipHash)
    print(btc_api.blockTipHeight)

    # Fetching info about genesis TX from the API
    tx_info = btc_api.tx(GENESIS_TX)
    current_block_height = btc_api.blockTipHeight

    catena.verifyTx(tx_info, current_block_height)
    


def calculator():
    print("Welcome to secure-calc!")






if __name__ == "__main__":
    print("Running update checker on start-up...")
    check_update()
    calculator()
