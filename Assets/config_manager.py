import os

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

    def remove_session(self, session_name):
        # Get the path to the session file
        session_file = os.path.join(self.config_dir, f"{session_name}.toml")

        # Check if the session file exists
        if not os.path.exists(session_file):
            print(f"sshman : Session '{session_name}' not found.")
            return

            # Remove the session file
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
            # Read the session data as a string
            session_data = file.read()

        return session_data

    def load_all_session_names(self):
        # Get a list of all files in the config directory
        files = os.listdir(self.config_dir)
        session_names = []
        for file in files:
            # Check if the file has the ".toml" extension
            if file.endswith(".toml"):
                # Extract the session name from the file name (remove the ".toml" extension)
                session_name = os.path.splitext(file)[0]
                session_names.append(session_name)
        return session_names
