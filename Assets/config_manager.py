import binascii
import os

PREFIX = "sshm_enc:"


def EncodeData(input_string):
    binary_data = input_string.encode('utf-8')
    hex_data = binascii.hexlify(binary_data).decode('utf-8')
    half_length = len(hex_data) // 2
    beginning_half = hex_data[:half_length]
    ending_half = hex_data[half_length:]
    transformed_hex_data = ending_half + beginning_half
    return PREFIX + transformed_hex_data


def DecodeData(hex_data):
    hex_data = hex_data[len(PREFIX):]  # Remove the prefix
    half_length = len(hex_data) // 2
    ending_half = hex_data[:half_length]
    beginning_half = hex_data[half_length:]
    transformed_hex_data = beginning_half + ending_half
    binary_data = binascii.unhexlify(transformed_hex_data)
    output_string = binary_data.decode('utf-8')
    return output_string


class ConfigManager:
    def __init__(self, config_dir=".sshm"):
        self.config_dir = os.path.expanduser(os.path.join("~", config_dir))

    def create_config_directory(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def save_session_info(self, session_name, data):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        with open(session_file, "w") as file:
            file.write(data)

    def export_session_info(self, session_name, export_dir):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        with open(session_file) as sfile:
            text = sfile.read()
            encoded = EncodeData(text)
        with open(f"{export_dir}{session_name}", "w") as file:
            file.write(encoded)

    def import_session_info(self, session_name, import_file):
        with open(import_file) as file:
            encoded_data = file.read().strip()
            decoded_data = DecodeData(encoded_data)
            self.save_session_info(session_name, decoded_data)

    def remove_session(self, session_name):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")

        if not os.path.exists(session_file):
            print(f"sshman : Session '{session_name}' not found.")
            return

        try:
            os.remove(session_file)
            print(f"sshman : Session '{session_name}' removed successfully.")
        except Exception as e:
            print(f"sshman : Error removing session '{session_name}': {str(e)}")

    def load_session_info(self, session_name):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        if not os.path.exists(session_file):
            return None

        with open(session_file, "r") as file:
            session_data = file.read()

        return session_data

    def load_all_session_names(self):
        files = os.listdir(self.config_dir)
        session_names = []
        for file in files:
            if file.endswith(".toml"):
                session_name = os.path.splitext(file)[0]
                session_names.append(session_name)
        return session_names
