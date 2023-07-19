#! /usr/bin/python3

import toml
import argparse

from Assets.config_manager import ConfigManager
from Assets.session_manager import SessionManager

def generate_session():
    # Get session details from user input
    session_name = input("sshman : how do you want to name this session? ")
    username = input("sshman : input the username: ")
    host = input("sshman : input the host: ")
    key_path = input("sshman : input the key path (leave blank for password authentication): ")

    # Example session data
    session_data = {
        "username": username,
        "host": host,
        "key": key_path if key_path else None,
    }

    # Convert the dictionary to a TOML string before encoding
    session_data_str = toml.dumps({"main-" + session_name: session_data})
    # Step 2: Save the encoded data to the config file
    config_manager = ConfigManager()
    config_manager.create_config_directory()
    config_manager.save_session_info(session_name, session_data_str)

    print("sshman : Success!")

def connect_session(session_name):
    # Step 1: Load the session data from the config file
    config_manager = ConfigManager()
    session_data_str = config_manager.load_session_info(session_name)
    if not session_data_str:
        print(f"sshman : Session '{session_name}' not found.")
        return

    # Step 2: Convert the session data back to a dictionary
    session_data = toml.loads(session_data_str)
    # Step 4: Build and run the SSH command
    session_manager = SessionManager()
    ssh_command = session_manager.connect_ssh(session_data, session_name)
    
def main():
    parser = argparse.ArgumentParser(description="SSH Session Manager")
    parser.add_argument("--generate-session", action="store_true", help="Generate a new SSH session")
    parser.add_argument("--connect", type=str, help="Connect to a saved SSH session by name")

    args = parser.parse_args()

    if args.generate_session:
        print("[ sshman : Generating session ]")
        generate_session()

    elif args.connect:
        print(f"[ sshman : Connecting to session '{args.connect}' ]")
        connect_session(args.connect)

if __name__ == "__main__":
    main()
