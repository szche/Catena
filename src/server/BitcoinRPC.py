from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

USER = 'user'
PASSWORD = '123'
WALLET_LABEL = 'Catena1'

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(USER, PASSWORD))

# Get the address of a Catena wallet
CatenaAddress = list(rpc_connection.getaddressesbylabel(WALLET_LABEL))[0]
CatenaAddressPrivKey = rpc_connection.dumpprivkey(CatenaAddress)
print(CatenaAddressPrivKey)
print('Found Catena address:', CatenaAddress)

# Combine all unspent UTXOs into one new Catena transaction
# Combining many UTXOs can be used for re-funding the "chain" of transactions
utxos = rpc_connection.listunspent()
CatenaInputs = []
CatenaOutputs = []
total_amount = Decimal(0)

for utxo in utxos:
	txid = utxo['txid']
	vout = utxo['vout']
	amount = utxo['amount']
	print(utxo)
	total_amount += amount 
	CatenaInputs.append( {'txid': txid, 'vout': vout} ) 

CatenaOutputs.append( {'data': '5465737420545821'} )
CatenaOutputs.append( {CatenaAddress: total_amount} )

print(CatenaInputs)
print(total_amount)

raw_tx = rpc_connection.createrawtransaction(CatenaInputs, CatenaOutputs)
signed_tx = rpc_connection.signrawtransactionwithkey(raw_tx, [CatenaAddressPrivKey])
print(signed_tx)


