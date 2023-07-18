import toml
import argparse
import base64
import hashlib

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

    # Step 1: Encrypt the session data
    encrypted_data = hashlib.md5(session_data_str.encode()).digest()

    # Step 2: Encode the encrypted data as base64
    encoded_data = base64.b64encode(encrypted_data).decode()

    # Step 3: Save the encoded data to the config file
    config_manager = ConfigManager()
    config_manager.create_config_directory()
    config_manager.save_session_info(session_name, {"data": encoded_data})

    print("sshman : Success!")

def connect_session(session_name):
    # Step 1: Load the encoded session data from the config file
    config_manager = ConfigManager()
    encoded_data = config_manager.load_session_info(session_name)
    if not encoded_data:
        print(f"sshman : Session '{session_name}' not found.")
        return

    # Step 2: Decode the encoded data from base64
    decoded_data = base64.b64decode(encoded_data.encode())

    # Step 3: Convert the decoded data back to bytes
    data_bytes = hashlib.md5(decoded_data).digest()

    # Step 4: Build and run the SSH command
    session_manager = SessionManager()
    ssh_command = session_manager.connect_ssh(toml.loads(data_bytes))
    print("sshman : Running SSH command:", ssh_command)

def main():
    parser = argparse.ArgumentParser(description="SSH Session Manager")
    parser.add_argument("--generate-session", action="store_true", help="Generate a new SSH session")
    parser.add_argument("--connect", type=str, help="Connect to a saved SSH session by name")

    args = parser.parse_args()

    if args.generate_session:
        print("[ sshman : Generating session ]")
        # Implement a fancy loading bar here to create the .sshm dir alongside a config file

        generate_session()

    elif args.connect:
        print(f"[ sshman : Connecting to session '{args.connect}' ]")
        connect_session(args.connect)

if __name__ == "__main__":
    main()
