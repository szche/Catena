from bitcoinlib.wallets import Wallet 
from bitcoinlib.wallets import wallets_list
from bitcoinlib.transactions import Output
from bitcoinlib.keys import Address
#from bitcoinlib.values import Value

NETWORK = 'testnet'
WALLET_NAME = 'Catena'

class Bitcoin():

		def __init__(self, network):
				self.network = network
				# Check if wallet named 'Catena' alerady exsits
				# Connects to it if so, creates it otherwise
				if self._check_if_exists(WALLET_NAME):
					self.wallet = self._connect_wallet(WALLET_NAME)
					self.wallet.balance_update_from_serviceprovider()
				else:
					self.wallet = self._create_wallet(WALLET_NAME)

		
		def _check_if_exists(self, name):
				wallets = wallets_list()
				for w in wallets:
						if w['name'] == name:
								return True
				return False
		
		def _create_wallet(self, name):
			return Wallet.create(name, network=self.network)

		def _connect_wallet(self, name):
			return Wallet(name)

		@property
		def balance(self):
			self.wallet.balance_update_from_serviceprovider()
			return self.wallet.balance()

		@property
		def address(self):
			return self.wallet.addresslist()[0]
	

		def new_log(self, hashed_data):
			self.wallet.utxos_update()
			len_data = len(hashed_data)
			len_data_hex = hex(len_data//2)[2:]
			lock_script = f'6a{len_data_hex}{hashed_data}'
			address = self.address
			# TODO smarter fee estimation
			# Currently fee = 700 sats
			fee = 700
			change_output = Output(value=self.balance-fee, address=address, network=self.network)
			catena_output = Output(0, script_type='nulldata', lock_script=lock_script, network=self.network)
			outputs = [change_output, catena_output]
			inputs = self.wallet.select_inputs(self.balance)
			tx = self.wallet.transaction_create(output_arr=outputs, \
							input_arr=inputs, network=self.network)
			tx.sign()
			# For debugging dont send it yet
			#tx.send()
			print(tx.info())




if __name__ == "__main__":
	btc = Bitcoin(NETWORK)
	print(btc.balance)
	print(btc.address)
	btc.new_log('9afbd907e01dae46f785a6db90cf1f9090158312f58b7cd67593c224ce17fc74')

