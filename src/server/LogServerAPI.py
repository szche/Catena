from flask import Flask, json, render_template, request, send_from_directory
from flask_httpauth import HTTPBasicAuth
from os import listdir, stat
from os.path import isfile, join

from database import Database
from merkletree import MerkleTree
from bitcoinrpc import Bitcoin, NETWORK

db = Database()
merkle_tree = MerkleTree()
btc = Bitcoin(NETWORK)
auth = HTTPBasicAuth()

# TODO store the tree in the file and dont re-calculate it on every server startup
latest_catena = btc.get_latest_catena_transaction()
for filehash in [x[6] for x in db.get_all()]:
	merkle_tree.add_child(filehash)
#print(merkle_tree)
update_path = 'database/files/'

api = Flask(__name__)
admin_credintials = ['admin', 'password']

@auth.verify_password
def verify_password(username, password):
	if username == admin_credintials[0] and password == admin_credintials[1]:
		return username


@api.route('/admin')
@auth.login_required
def admin_panel():
	merkle_root = merkle_tree.get_root()
	latest_file = db.get_all()[-1]
	proof = merkle_tree.get_proof(latest_file[6])
	proof_str = ""
	wallet_balance = btc.balance_cache / 100000000
	wallet_address = btc.address
	for level in proof:
		proof_str += f'{level[0]} - {level[1]}\n'
	return render_template('index.html', merkle_root=merkle_root, \
			latest_file=latest_file, \
			merkle_proof=proof_str, \
			balance=wallet_balance, \
			address=wallet_address)


@api.route('/push-new-root')
@auth.login_required
def push_new_root():
	all_db_files = db.get_all()
	# Craft a new local merkle tree with all the files in database and publish the digest to the Bitcoin network
	local_tree = MerkleTree()
	for fileinfo in all_db_files:
		local_tree.add_child(fileinfo[6])
	print("New merkle root: ", local_tree.get_root())
	# Save the tree
	local_tree.save_tree( local_tree.get_root() )
	# Publish new root to the network
	print(btc.new_log( local_tree.get_root() ))
	return 'Ok', 200




@api.route('/all', methods=['GET'])
def get_all():
	files = db.get_all()
	response = api.response_class(
				response=json.dumps( files ),
				status=200,
				mimetype='application/json')
	return response 

@api.route('/download', methods=['GET'])
def get_file_by_hash():
	file_hash = request.args.get("file")
	database_search = db.get_by_hash(file_hash)
	# Send empty response if no file found
	if database_search == []:
		return 'Not found', 404
	else:
		file_info = database_search[0]
		file_name = file_info[1]
		response = send_from_directory(directory=update_path, path=file_name)
		return response, 200

@api.route('/verify', methods=['GET'])
def verify_file():
	file_hash = request.args.get("file")
	database_search = db.get_by_hash(file_hash)
	# Send empty response if no file found
	if database_search == []:
		return 'Not found', 404
	else:
		proof = merkle_tree.get_proof(file_hash)
		response = api.response_class(
				response=json.dumps( proof ),
				status=200,
				mimetype='application/json')
		return response 


"""
1) Api Admina (upload pliku na serwer, podpisywanie pliku, dodanie pliku do bazy danych, drzewa merkle, transakcji Bitcoin)
2) w /admin przesłać do template dodatkowe informacje (stan portfela bitcoin, ile plików w bazie danych, itp.)
"""

if __name__ == '__main__':
    api.run(debug=True)
