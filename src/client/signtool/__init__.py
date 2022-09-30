import subprocess
import hashlib

class SignTool:
    """ Class for extracting and verifying signature from signed binary.
    Uses Powershell's Get-AuthenticodeSignature command
    """

    def _run_powershell_cmd(self, filepath):
        """ Runs Get-AuthenticodeSignature powershell commmand
        with given filepath. Returns (returncode, output) tuple"""
        command = f'Get-AuthenticodeSignature {filepath} | \
                Format-List -Property \
                SignerCertificate,TimeStamperCertificate,Status, \
                StatusMessage,Path,SignatureType,IsOSBinary'
        output = subprocess.run(["powershell", "-Command", command],
                                capture_output=True)
        if output.returncode == 1:
            return (output.returncode, output.stderr.decode('windows-1252'))
        return (output.returncode, output.stdout.decode('windows-1252'))

    def _parse_output(self, output):
        """ Parses the Powershell's command to extract signature status\
        and signature thumpbrint.
        Returns dictionary conatining status and thumbprint of a binary.
        If signature is invalid, no thumbprint is returned.
        """
        data = {}
        # Check if Status if Valid, if not return just the status
        status_pos = output.find("Status")
        status_endline = output[status_pos:].find('\n')
        data['status'] = output[status_pos:status_pos+status_endline]
        data['status'] = data['status'].split(':')[1].strip()
        if data['status'] != 'Valid':
            return data
        # Get signagure issuer
        subject_pos = output.find("[Subject]")
        sig_issuer = output[subject_pos+len("[Subject]"):].strip()
        issuer = sig_issuer.split("\n")[0].strip()
        data['issuer'] = issuer

        # Get thumbprint of a signer pubkey
        thumbprint_pos = output.find("[Thumbprint]")
        data['thumbprint'] = output[thumbprint_pos:].split('\n')[1].strip()

        # Get issuer BTC address from description - experimental way of transfer address
        # TODO

        return data

    def verify(self, filepath):
        """ Method to interact with class, takes the filepath as an argument.
        Method runs powershell command, parses the output
        and returns information.
        Returns dictionary containing status, thumbprint and filepath.
        If signature is invalid, no thumbprint is returned """
        powershell_output = self._run_powershell_cmd(filepath)
        # if error occcured during powershell command, return error status
        if powershell_output[0] != 0:
            return {
                    'status': 'Error during Get-AuthenticodeSignature',
                    'path': filepath
                    }
        parsed_output = self._parse_output(powershell_output[1])
        parsed_output['path'] = filepath
        return parsed_output

    def extract_btc_address(self, filepath):
        command = f'certutil.exe -dump {filepath} | Select-String Description'
        output = subprocess.run(["powershell", "-Command", command],
                                capture_output=True)
        if output.returncode == 1:
            return (output.returncode, output.stderr.decode('windows-1252'))

        #return (output.returncode, output.stdout.decode('windows-1252'))
        decoded = output.stdout.decode('windows-1252')
        decoded = decoded.replace("\n", "").replace("\r","").replace("'","").replace(")","").replace(" ","")
        decoded = decoded[decoded.find("D"):].split(":")
        return decoded[1]

    def get_hash_of_file(self, file_path):
        sha2 = hashlib.sha256()
        with open(file_path, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest()
            return readable_hash

if __name__ == '__main__':
    signtool = SignTool()
    #print(signtool.verify("D:\\VSCodeUserSetup-x64-1.55.2.exe"))
    print(signtool.extract_btc_address(r"D:\Catena-supply\podpisana-binarkav2.exe"))
    print(signtool.get_hash_of_file(r"D:\Catena-supply\podpisana-binarkav2.exe"))