import subprocess

class SignTool():
		def __init__(self):
				pass

		def _run_command(self, cmd):
				c = subprocess.run(cmd, capture_output=True, shell=True)
				# Return code 0 is success 
				# TODO files without signatures also return 0
				if c.returncode == 0:
					print(c.stdout)
					return True
				print('-'* 20)
				print("ERROR")
				print(c.stderr.decode())
				print('-'* 20)
				return False


		def sign(self, certfile, keyfile, description, url, filepath, filepath_signed):
				# Needs to be executed with sudo to be working correctly
				command = f'osslsigncode sign -h sha2 -certs {certfile} ' + \
							f'-key {keyfile} -n {description} -i {url} ' + \
							f'-in {filepath} -out {filepath_signed}'
				print('Final command: ', command)
				print( self._run_command(command) )

		def verify(self, filepath):
				command = f'osslsigncode verify {filepath}'
				print( self._run_command(command) )


if __name__ == "__main__":
		signer = SignTool()
		signer.sign('/home/sh/Desktop/Catena/selfsigned.crt','/home/sh/Desktop/Catena/selfsigned.key','123', \
						'https://google.pl','/home/sh/Desktop/Catena/sample_to_sign.exe','/home/sh/Desktop/Catena/sample_signed.exe')
		signer.verify('/home/sh/Desktop/Catena/sample_signed.exe')
		signer.verify('/home/sh/Desktop/Catena/sample_to_sign.exe')
