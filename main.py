import os
from cryptography.fernet import Fernet

from Assets.config_manager import Save_Config, Load_Config
from Assets.cryptography_manager import Encrypt, Decrypt

key = Fernet.generate_key()
ssh_manager_config = os.path.expanduser("~/.sshm")  # Using os.path.expanduser to get the user's home directory

# Setting Encrypt/Decrypt classes
encm = Encrypt(key)
decm = Decrypt(key)

confl = Load_Config()  # Config Load
confs = Save_Config()  # Config Save

# Ensuring .sshm folder exists
if not os.path.exists(ssh_manager_config):
    print("[ssh manager] : Generating .sshm folder in $HOME")
    os.makedirs(ssh_manager_config)

# Saving key
key_file_path = os.path.join(ssh_manager_config, "pepper.reppep")
confs.save(key_file_path, key)

# Loading key
loaded_key = confl.load(key_file_path)
print("[ssh manager] : Loaded saved config.")


# Testing

key_file_path = os.path.join(ssh_manager_config, "pepper.reppep")
confs.save(key_file_path, "example_session", "/home/auth/.ssh/hexis.pem", "ubuntu", "3.96.133.216", None, None)

loaded_key = confl.load(key_file_path, "example_session")
print(loaded_key)