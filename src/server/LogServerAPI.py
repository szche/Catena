from flask import Flask, json, render_template, request, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import os.path

from database import Database, calculate_file_hash
from merkletree import MerkleTree
from bitcoinrpc import Bitcoin, NETWORK
from signtool import SignTool



db = Database()
merkle_tree = MerkleTree()
btc = Bitcoin(NETWORK)
auth = HTTPBasicAuth()

# TODO store the tree in the file and dont re-calculate it on every server startup
# Find the latest catena hash commit and load the merkle-tree file
latest_catena = btc.get_latest_catena_transaction()
merkle_tree.load_tree( latest_catena['op_return_hash'] )
#for filehash in [x[6] for x in db.get_all()]:
#	merkle_tree.add_child(filehash)
#print(merkle_tree)
update_path = 'database/files/'
upload_path = 'uploads/'

api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = upload_path


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

@api.route('/uploader', methods = ['POST'])
@auth.login_required
def upload_file():
	f = request.files['file']
	path_to_upload = os.path.join(api.config['UPLOAD_FOLDER'], secure_filename(f.filename))
	path_to_store_signed = os.path.join(update_path, secure_filename(f.filename))
	f.save(path_to_upload)
	# Sign the file
	signer = SignTool()
	signing = signer.sign('/home/sh/Desktop/Catena/selfsigned.crt','/home/sh/Desktop/Catena/selfsigned.key','123', \
						'https://google.pl', path_to_upload, path_to_store_signed)
	if signing == False:
		return "Erorr signing file"
	
	# Add to the database
	file_hash = calculate_file_hash(path_to_store_signed)
	db.add_new_binary(secure_filename(f.filename), '1', '10-05-2022', '10-05-2022', 20, file_hash, 'WIN')

	# Create new merkle tree
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
	print("User looking to download file with hash: ", file_hash)
	database_search = db.get_by_hash(file_hash)
	print(database_search)
	# Send empty response if no file found
	if len(database_search) == 0:
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
		proof = []
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
