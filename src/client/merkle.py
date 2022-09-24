import typing
import ast
import hashlib
from typing import List

class MerkleClient():
	def __init__(self):
		pass

	def sha256(self, data: str) -> str:
		return hashlib.sha256(data.encode('utf-8')).hexdigest()

	def string_to_list_list(self, string: str):
		return ast.literal_eval(string)

	def count_root(self, item: str, proof: List[List[str]]) -> str:
		 # lekkie zabezpieczenie
		if type(proof) == type("string"):
			proof = ast.literal_eval(proof)

		final_hash = item
		for step in proof:
			direction, hashed_data = step[0], step[1]
			if direction == 'left':
				final_hash = self.sha256(final_hash+hashed_data)
			elif direction == 'right':
				final_hash = self.sha256(hashed_data+final_hash)
			elif direction == 'up':
				continue
		return final_hash
