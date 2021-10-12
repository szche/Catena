from flask import Flask, json
from os import listdir, stat
from os.path import isfile, join
import hashlib

update_path = 'update/'

api = Flask(__name__)

# Calculate SHA-256 of file
def sha256_file(path):
	sha256_hash = hashlib.sha256()
	with open(path,"rb") as f:
		for byte_block in iter(lambda: f.read(4096),b""):
			sha256_hash.update(byte_block)
	return sha256_hash.hexdigest()

def find_update_file():
	update_file = {
			'filename': None,
			'date': 0,
			'hash': None,
			'merkle_proof': None}
	for f in listdir(update_path):
		if not isfile(join(update_path, f)):
			continue
		if stat(join(update_path, f)).st_mtime > update_file['date']:
			update_file['filename'] = f
			update_file['date'] = stat(join(update_path, f)).st_mtime
	
	update_file['hash'] = sha256_file( join(update_path, update_file['filename']) )
	print(update_file)
	return update_file

@api.route('/update', methods=['GET'])
def get_update():
	find_update_file()
	response = api.response_class(
				response=json.dumps( find_update_file() ),
				status=200,
				mimetype='application/json')
	return response 

#TODO
@api.route('/verify', methods=['GET'])
def verify():
	pass

if __name__ == '__main__':
    api.run()
