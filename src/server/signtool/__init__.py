import subprocess

class SignTool():
		def _run_command(self, cmd):
				c = subprocess.run(cmd, capture_output=True, shell=True)
				#print(c)
				# Return code 0 is success 
				if c.returncode == 0 and "No signature found" not in c.stdout.decode():
					#print(c.stdout.decode())
					return True
				#print('-'* 20)
				#print("ERROR")
				#print(c.stderr.decode())
				#print('-'* 20)
				return False

		def sign(self, certfile, keyfile, description, url, filepath, filepath_signed):
				# Needs to be executed with sudo to be working correctly
				command = f'osslsigncode sign -h sha2 -certs {certfile} ' + \
							f'-key {keyfile} -n {description} -i {url} ' + \
							f'-in {filepath} -out {filepath_signed}'
				#print('Final command: ', command)
				return self._run_command(command)

		def verify(self, filepath):
				command = f'osslsigncode verify {filepath}'
				return self._run_command(command)


if __name__ == "__main__":
		signer = SignTool()
		signer.sign('/home/sh/Desktop/Catena/selfsigned.crt','/home/sh/Desktop/Catena/selfsigned.key','123', \
						'https://google.pl','/home/sh/Desktop/Catena/sample_to_sign.exe','/home/sh/Desktop/Catena/sample_signed.exe')
		signer.verify('/home/sh/Desktop/Catena/sample_signed.exe')
		signer.verify('/home/sh/Desktop/Catena/sample_to_sign.exe')

