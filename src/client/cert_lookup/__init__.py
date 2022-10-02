import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class CertLookup:
    def __init__(self):
        self.ssl = ssl.create_default_context()
        self.certificates = []
        self.gather_certs()

    def find_by_thumbprint(self, thumbprint):
        for cert in self.certificates:
            if cert['thumbprint'] == thumbprint:
                return cert
        return False

    def hex_string_readable(self, bytes):
        return ["{:02X}".format(x) for x in bytes]

    def gather_certs(self):
        ca_certs = self.ssl.get_ca_certs(binary_form=True)
        for cert_binary in ca_certs:
            c = {}
            cert_pem = ssl.DER_cert_to_PEM_cert(cert_binary)
            certificate = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())
            thumbprint = self.hex_string_readable(certificate.fingerprint(hashes.SHA1()))
            thumbprint = ''.join(thumbprint)
            issuer = certificate.issuer.rfc4514_string()
            subject = certificate.subject.rfc4514_string()
            serial_number = hex(certificate.serial_number).replace("0x", "")
            issued_date = certificate.not_valid_before
            expiry_date = certificate.not_valid_after
            c['thumbprint'] = thumbprint.lower()
            c['issuer'] = issuer
            c['subject'] = subject
            c['serial_number'] = serial_number
            c['issued_date'] = issued_date
            c['expiry_date'] = expiry_date
            self.certificates.append(c)



if __name__ == "__main__":
    cert = CertLookup()
    #print(cert.find_by_thumbprint('ee869387fffd8349ab5ad14322588789a457b012'))
    print("\n\n\n\n")
    print(cert.find_by_thumbprint('cabd2a79a1076a31f21d253635cb039d4329a5e8'))