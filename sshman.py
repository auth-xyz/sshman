#! /usr/bin/python3
import os
import shutil
import tarfile

import toml
import argparse
from requests import get
from Assets.config_manager import ConfigManager
from Assets.session_manager import SessionManager

gh_username, repository = "auth-xyz", "sshman"


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


def connect_session(session_name, port_forwarding=False):
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


def list_sessions():
    # Step 1: Load the names of all available sessions from the config file
    config_manager = ConfigManager()
    session_names = config_manager.load_all_session_names()

    if not session_names:
        print("[ sshman : No sessions found. ]")
        return

    # Step 2: Print the names of all available sessions
    print("[ sshman: Available sessions: ]")
    for session_name in session_names:
        print(f"- {session_name}")


def download_latest(user: str, repo: str, path="./"):
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    response = get(url)

    if response.status_code == 200:
        release_data = response.json()
        asset = release_data["assets"][0]  # Assuming the first asset is the latest release

        download_url = asset["browser_download_url"]
        filename = os.path.join(path, asset["name"])

        # Download the asset file
        with get(download_url, stream=True) as download_response:
            download_response.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"[ sshman: Successfully downloaded {asset['name']} to {path} ]")

        # Extract the downloaded .tar.gz file
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall(path=path)

        # Move sshman file to ~/.sshm/.bin/ and replace if it already exists
        extracted_folder = os.path.splitext(asset["name"])[0]
        extracted_sshman = os.path.join(path, "dist", "sshman")
        target_sshman = os.path.expanduser("~/.sshm/.bin/sshman")

        if os.path.exists(target_sshman):
            os.remove(target_sshman)

        shutil.move(extracted_sshman, target_sshman)
        print("[ sshman: Moved binary to .sshm/.bin/ ]")

        # Clean up the extracted folder
        shutil.rmtree(os.path.join(path, "dist/"))
        if os.path.exists(filename):
            os.remove(filename)
        print("[ sshman: Cleaned up extracted files. ]")
    else:
        print(f"[ sshman: Failed to fetch release data. Status code: {response.status_code} ]")


def main():
    parser = argparse.ArgumentParser(description="SSH Session Manager")
    parser.add_argument("-G", "--generate-session", action="store_true", help="Generate a new SSH session")
    parser.add_argument("-ls", "--sessions", help="Outputs all sessions", action="store_true")
    parser.add_argument("-C", "--connect", type=str, help="Connect to a saved SSH session by name")
    parser.add_argument("-R", "--remove-session", type=str, help="Removes a session")
    parser.add_argument("-u", "--update", help="Downloads the latest compiled version and installs it",
                        action="store_true")

    args = parser.parse_args()

    if args.generate_session:
        print("[ sshman : Generating session ]")
        generate_session()
    elif args.update:
        print(f"[ sshman : Downloading latest version of sshman... ]")
        download_latest(gh_username, repository, path="./")
    elif args.connect:
        print(f"[ sshman : Connecting to session '{args.connect}' ]")
        connect_session(args.connect)
    elif args.sessions:
        list_sessions()
    elif args.remove_session:
        print(f"[ sshman : Removing session '{args.remove_session}' ]")
        config_manager = ConfigManager()
        config_manager.remove_session(args.remove_session)
    else:
        print("[ sshman : No valid option selected. Use --help for usage details. ]")


if __name__ == "__main__":
    main()
