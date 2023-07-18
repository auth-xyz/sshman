import os
import toml
from cryptography_manager import Decrypt, Encrypt

with open(os.path.expanduser(".sshm/pepper.reppep"), "rb") as key_file:
    key_file.read()
    key = key_file

encm = Encrypt(key)
decm = Decrypt(key)

class Save_Config():
    def __init__(self, key):
        self.key = key
    
    def save(self, filename, session_name, host, address, command, arguments):
        data = {
            f"main-{session_name}": {
                "key": self.key,
                "host": host,
                "address": address,
                "command": command,
                "arguments": arguments
            }
        }
        encrypted_data = toml.dumps(data).encode()
        encm.encrypt_file(filename, encrypted_data)
    
class Load_Config():
    def __init__(self):
        pass
    
    def load(self, filename, session_name):
        encrypted_data = decm.decrypt_file(filename)
        data = toml.loads(encrypted_data.decode())
        session_key = data[f"main-{session_name}"]["key"]
        return session_key
    