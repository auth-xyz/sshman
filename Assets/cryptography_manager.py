from cryptography.fernet import Fernet

class Encrypt():
    def __init__(self, key):
        self.key = key

    def encrypt_file(self, filename, data):
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(data.encode())
        with open(filename, 'wb') as file:
            file.write(encrypted_data)

class Decrypt():
    def __init__(self, key):
        self.key = key

    def decrypt_file(self, filename):
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data.decode()
    