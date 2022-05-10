from flask import Flask, json, render_template, request, send_from_directory
from os import listdir, stat
from os.path import isfile, join

from database import Database
from merkletree import MerkleTree

db = Database()
merkle_tree = MerkleTree()

# TODO store the tree in the file and dont re-calculate it on every server startup
for filehash in [x[6] for x in db.get_all()]:
	merkle_tree.add_child(filehash)
print(merkle_tree)
update_path = 'database/files/'

api = Flask(__name__)

@api.route('/admin')
def admin_panel():
	merkle_root = merkle_tree.get_root()
	latest_file = db.get_all()[-1]
	proof = merkle_tree.get_proof(latest_file[6])
	proof_str = ""
	for level in proof:
		proof_str += f'{level[0]} - {level[1]}\n'
	return render_template('index.html', merkle_root=merkle_root, latest_file=latest_file, merkle_proof=proof_str)

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
    api.run()
