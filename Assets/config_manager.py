import binascii
import os

PREFIX = "sshm_enc:"
CONFIG_DIR = ".sshm"


class ConfigManager:
    def __init__(self, config_dir=None):
        self.config_dir = os.path.expanduser(os.path.join("~", config_dir or CONFIG_DIR))

    @staticmethod
    def _encode_data(input_string):
        binary_data = input_string.encode('utf-8')
        hex_data = binascii.hexlify(binary_data).decode('utf-8')
        transformed_hex_data = hex_data[-len(hex_data) // 2:] + hex_data[:len(hex_data) // 2]
        return PREFIX + transformed_hex_data

    @staticmethod
    def _decode_data(hex_data):
        hex_data = hex_data[len(PREFIX):]
        transformed_hex_data = hex_data[-len(hex_data) // 2:] + hex_data[:len(hex_data) // 2]
        binary_data = binascii.unhexlify(transformed_hex_data)
        output_string = binary_data.decode('utf-8')
        return output_string

    def create_config_directory(self):
        try:
            os.makedirs(self.config_dir, exist_ok=True)
        except Exception as e:
            print(f"sshman : Error creating config directory: {str(e)}")

    def save_session_info(self, session_name, data):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        try:
            with open(session_file, "w") as file:
                file.write(data)
        except Exception as e:
            print(f"sshman : Error saving session '{session_name}': {str(e)}")

    def export_session_info(self, session_name, export_dir):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        try:
            with open(session_file, "r") as file:
                encoded = self._encode_data(file.read().strip())
            export_path = os.path.join(export_dir, session_name)
            with open(export_path, "w") as file:
                file.write(encoded)
        except Exception as e:
            print(f"sshman : Error exporting session '{session_name}': {str(e)}")

    def import_session_info(self, session_name, import_file):
        try:
            with open(import_file, "r") as file:
                decoded_data = self._decode_data(file.read().strip())
            self.save_session_info(session_name, decoded_data)
        except Exception as e:
            print(f"sshman : Error importing session from '{import_file}': {str(e)}")

    def remove_session(self, session_name):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        try:
            os.remove(session_file)
            print(f"sshman : Session '{session_name}' removed successfully.")
        except FileNotFoundError:
            print(f"sshman : Session '{session_name}' not found.")
        except Exception as e:
            print(f"sshman : Error removing session '{session_name}': {str(e)}")

    def load_session_info(self, session_name):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        try:
            with open(session_file, "r") as file:
                session_data = file.read()
            return session_data
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"sshman : Error loading session '{session_name}': {str(e)}")

    def load_all_session_names(self):
        try:
            files = os.listdir(self.config_dir)
            session_names = [os.path.splitext(file)[0] for file in files if file.endswith(".toml")]
            return session_names
        except Exception as e:
            print(f"sshman : Error loading session names: {str(e)}")
            return []
