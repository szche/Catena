import requests

class BitcoinAPI(object):
    """
     Using Blockstream's API
     https://github.com/Blockstream/esplora/blob/master/API.md
    """
    def __init__(self):
        self.url_test = 'https://blockstream.info/testnet/api/'
        self.url = 'https://blockstream.info/api/' # na potrzeby testów
    

    def __block(self, endpoint):
        r = requests.get(f'{self.url_test}blocks/{endpoint}')
        return r

    def address_txs(self, address):
        r = requests.get(f'{self.url_test}address/{address}/txs')
        json_string = r.json()
        return json_string

    @property
    def blockTipHash(self):
        return self.__block('tip/hash').text

    @property
    def blockTipHeight(self):
        return int(self.__block('tip/height').text)

    def tx(self, txhash):
        r = requests.get(f'{self.url_test}/tx/{txhash}')
        json_string = r.json()
        return json_string

    @staticmethod
    def extract_OP_RETURNs_blockHash_from_txs(txs_output_api):
        """
            param: Dict: txs
            TODO


            obj_tx structure:
            {
                "txid": ID of tx,
                "tx_status":{
                    "confirmed": is if confirmed?
                    "block_height": block height
                    "tx_status": status of the tx,
                    "block_hash": hash of the transaction block,
                    "block_time": time of the block
                },
                "op_return": OP_RETURN of the transaction,
            }
        """
        op_returns = []
        for tx in txs_output_api:
            out_txs = tx["vout"]
            
            out_txs_with_op_returns = list(filter(lambda tx: tx["scriptpubkey_type"] == "op_return", out_txs))

            #print(out_txs_with_op_returns)
            if len(out_txs_with_op_returns) > 0:
                obj_tx = {
                    "txid": tx["txid"],
                    "tx_status": tx["status"],
                    "op_return": out_txs_with_op_returns[0]["scriptpubkey_asm"].split(" ")[2]
                }
                op_returns.append(obj_tx)


        return op_returns

    def get_OPs(self, address):
        return self.extract_OP_RETURNs_blockHash_from_txs(self.address_txs(address))


if __name__ == "__main__":
    api = BitcoinAPI()
    #api.block()
    #api.tx('13c7ef106183ced5a2119b2a46670988dd456c82cc3c87318d8e8c5cba2c3ac1')
    #json_string = api.tx('ce50a89a3469141d3ece3d74da9a726902bcb27850a1f4122ca7079964d609e7')
    json_string = api.address_txs("64b144ada7c8287535867b665299e7478a7e710ff8b83082236cf57020fc33af")
    print(json_string)
    #print(api.get_OPs("mwN99uG9Qgabo8JwL4VKQqNST3odzyQBg8"))





