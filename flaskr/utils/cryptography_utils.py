from cryptography.fernet import Fernet


class CryptographyUtils:
    _cipher_suite: Fernet

    def __init__(self, encryption_key: str):
        self._cipher_suite = Fernet(encryption_key)

    def encrypt(self, value: str) -> str:
        value_as_bytes = value.encode('utf-8')
        return self._cipher_suite.encrypt(value_as_bytes).decode()

    def decrypt(self, value: str) -> str:
        value_as_bytes = value.encode('utf-8')
        return self._cipher_suite.decrypt(value_as_bytes).decode()
