from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
from config import BITCOIN_RPC_USER, BITCOIN_RPC_PASS, BITCOIN_WALLET_LABEL


class BitcoinRPC(object):

	def __init__(self, user, password, wallet_label):
		self.rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(user, password))
		# Address for Catena wallet
		self.catena_public = list(self.rpc_connection.getaddressesbylabel(wallet_label))[0]
		# Private key used for signing new transactions
		self.catena_private = self.rpc_connection.dumpprivkey(self.catena_public)
		print("Catena public address:", self.short_key(self.catena_public))
		print("Catena private key: ", self.short_key(self.catena_private))


	def short_key(self, key):
		return key[:6] + '...' +  key[-6:]

	#Creates new Catena transaction and returns signed tx
	def new_log(self, data):
		utxos = self.rpc_connection.listunspent()
		inputs = []
		outputs = []
		total_amount = Decimal(0)

		# Combine all unspent UTXOs into one new Catena transaction
		# Combining many UTXOs can be used for re-funding the "chain" of transactions
		for utxo in utxos:
			txid = utxo['txid']
			vout = utxo['vout']
			amount = utxo['amount']
			print(utxo)
			total_amount += amount 
			inputs.append( {'txid': txid, 'vout': vout} ) 

		#TODO This is the OP_RETURN output
		# Put merkle tree root here
		outputs.append( {'data': data} )

		#TODO Calculate fee neded to add the tx within 1 block
		# bitcoin-cli estimatesmartfee 1
		# fee = ????
		# Send the rest of money back to yourself (without the fee cost)
		outputs.append( {self.catena_public: total_amount} )

		print(inputs)
		print(total_amount)

		raw_tx = self.rpc_connection.createrawtransaction(inputs, outputs)
		signed_tx = self.rpc_connection.signrawtransactionwithkey(raw_tx, [self.catena_private])
		print(signed_tx)
		return signed_tx

	#Broadcasts signed transaction to the network
	def broadcast_tx(self, tx):
		pass

	#Returns current block height
	def get_blockchain_info(self):
		blockchain = self.rpc_connection.getblockchaininfo()
		print(blockchain)
		return blockchain

	#Returns balance of the wallet
	def get_balance(self):
		pass

	#Returns all spending history
	def get_tx_history(self):
		pass

if __name__ == "__main__":
	rpc = BitcoinRPC(BITCOIN_RPC_USER, BITCOIN_RPC_PASS, BITCOIN_WALLET_LABEL)
	rpc.get_blockchain_info()
	#rpc.new_log('5369656d6b6120636f2074616d')
