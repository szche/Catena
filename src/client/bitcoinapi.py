import requests

class BitcoinAPI(object):
    """
     Using Blockstream's API
     https://github.com/Blockstream/esplora/blob/master/API.md
    """
    def __init__(self):
        self.url = 'https://blockstream.info/testnet/api/'
    

    def __block(self, endpoint):
        r = requests.get(f'{self.url}blocks/{endpoint}')
        return r

    @property
    def blockTipHash(self):
        return self.__block('tip/hash').text

    @property
    def blockTipHeight(self):
        return int(self.__block('tip/height').text)

    def tx(self, txhash):
        r = requests.get(f'{self.url}/tx/{txhash}')
        json_string = r.json()
        return json_string




if __name__ == "__main__":
    api = BitcoinAPI()
    api.block()
    print()
    api.tx('13c7ef106183ced5a2119b2a46670988dd456c82cc3c87318d8e8c5cba2c3ac1')









