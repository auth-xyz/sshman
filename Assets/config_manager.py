import os
import toml

class ConfigManager:
    def __init__(self, config_dir=".sshm"):
        self.config_dir = os.path.expanduser(os.path.join("~", config_dir))

    def create_config_directory(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def save_session_info(self, session_name, data):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        with open(session_file, "w") as file:
            # Save the data directly as a string
            file.write(data)

    def load_session_info(self, session_name):
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")
        if not os.path.exists(session_file):
            return None

        with open(session_file, "r") as file:
            # Read the session data as a string
            session_data = file.read()

        return session_data
    