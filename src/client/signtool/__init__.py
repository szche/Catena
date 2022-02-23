import os
import subprocess


class SignTool:
    
    def run_powershell_cmd(self, filepath):
        command = f'Get-AuthenticodeSignature {filepath} | Format-List -Property SignerCertificate,TimeStamperCertificate,Status,StatusMessage,Path,SignatureType,IsOSBinary'
        output = subprocess.run(["powershell", "-Command", command], capture_output=True)
        if output.returncode == 1:
            return (output.returncode, output.stderr.decode('windows-1252'))
        return (output.returncode, output.stdout.decode('windows-1252'))

    def parse_output(self, output):
        data = {}
        #Check if Status is Valid
        status_pos = output.find("Status")
        status_endline = output[status_pos:].find('\n')
        data['status'] = output[status_pos:status_pos+status_endline].split(':')[1].strip()
        if data['status'] != 'Valid':
            print('This signature is not valid!')
            return
        # Get thumbprint of a signer pubkey
        thumbprint_pos = output.find("[Thumbprint]")
        data['thumbprint'] = output[thumbprint_pos:].split('\n')[1].strip()
        print(data)
        return data
    
    def verify(self, filepath):
        powershell_output = self.run_powershell_cmd(filepath)
        #print(powershell_output[1])
        self.parse_output(powershell_output[1])


if __name__ == '__main__':
    signtool = SignTool()
