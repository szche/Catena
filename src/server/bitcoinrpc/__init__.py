from bitcoinlib.wallets import Wallet 
from bitcoinlib.wallets import wallets_list
from bitcoinlib.transactions import Output
from bitcoinlib.keys import Address
from bitcoinlib.scripts import Script

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
				self.balance
				self.cached_address = self.address

		
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
			self.balance_cache = self.wallet.balance()
			return self.balance_cache

		@property
		def address(self):
			self.address_cache = self.wallet.addresslist()[0]
			return self.address_cache
	

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
			tx.send()
			print(tx.info())

		def get_latest_catena_transaction(self):
			self.wallet.transactions_update()
			all_confirmed_txs = self.wallet.transactions(as_dict=True)
			if len(all_confirmed_txs) == 0:
				print("No transactions found")
				return False
			latest_tx = None
			for tx in all_confirmed_txs[::-1]:
				if tx['status'] != 'confirmed': continue
				db_tx = tx['transaction']
				db_tx_inputs = db_tx.inputs
				if db_tx_inputs is None: continue
				for tx_input in db_tx_inputs:
					if tx_input.address == self.cached_address:
						latest_tx = tx
						break
				if latest_tx != None: break
			if latest_tx == None:
				print("No catena TX found")
				return False
			latest_tx = self.wallet.transaction( latest_tx['txid'] )
			op_return_output = None
			for output in latest_tx.outputs:
				output_dict = output.as_dict()
				if output_dict['script_type'] == 'nulldata':
					op_return_output = output_dict
					break

			op_return_script = op_return_output['script']
			
			op_return_data = Script.parse(op_return_script).serialize_list()[-1].hex()

			return_data = {
				'txid': latest_tx.txid,
				'op_return_hash': op_return_data
			}
			return return_data



if __name__ == "__main__":
	btc = Bitcoin(NETWORK)
	#print(btc.wallet.info(detail=5))
	print(btc.get_latest_catena_transaction())
	#print(btc.balance)
	print(btc.address)

	#btc.new_log('08378b4527c8152aaefa8e251c2513ce8741c710229e79ae14a804b7a590da37')

