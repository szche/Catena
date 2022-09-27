import subprocess
import os

class SignTool():

		def __init__(self, path):
			# check if cert file and private key exists
			# if not, create them
			if self.check_if_exists(path) == False:
				print("CREATING!")
				self.createCertAndKey(path)
			

		def _run_command(self, cmd):
				c = subprocess.run(cmd, capture_output=True, shell=True)
				# Return code 0 is success 
				if c.returncode == 0 and "No signature found" not in c.stdout.decode():
					#print(c.stdout.decode())
					return True
				#print('-'* 20)
				#print("ERROR")
				#print(c.stderr.decode())
				#print('-'* 20)
				return False

		def sign(self, path, description, url, filepath, filepath_signed):
				# Needs to be executed with sudo to be working correctly
				command = f'osslsigncode sign -h sha2 -certs {path}keys/cert.crt ' + \
							f'-key {path}keys/private.key -n {description} -i {url} ' + \
							f'-in {filepath} -out {filepath_signed}'
				#print('Final command: ', command)
				return self._run_command(command)

		def verify(self, filepath, certpath):
				command = f'osslsigncode verify -in {filepath} -CAfile {certpath}'
				return self._run_command(command)

		def createCertAndKey(self, path):
			command = f'openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout {path}keys/private.key -out {path}keys/cert.crt -subj \'/CN=AGH/O=AGH/C=PL\''
			return self._run_command(command)

		def check_if_exists(self, path):
			files = os.listdir(f"{path}keys/")
			if 'private.key' in files and 'cert.crt' in files:
				return True
			return False 


if __name__ == "__main__":
		signer = SignTool()
		signer.sign('/home/szch/Desktop/Catena/selfsigned.crt','/home/szch/Desktop/Catena/private.key','123', \
						'https://google.pl','/home/szch/Desktop/Catena/2.exe','/home/szch/Desktop/Catena/sample_signed.exe')
		#print("Signed!")
		signer.verify('/home/szch/Desktop/Catena/sample_signed.exe', 'home/szch/Desktop/Catena/selfsigned.crt')
		signer.verify('/home/szch/Desktop/Catena/sample_to_sign.exe', 'home/szch/Desktop/Catena/selfsigned.crt')

