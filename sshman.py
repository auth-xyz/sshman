#! /usr/bin/python3
import os
import shutil
import tarfile
import platform

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

    session_data = {
        "username": username,
        "host": host,
        "key": key_path if key_path else None,
    }

    session_data_str = toml.dumps({"main-" + session_name: session_data})
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

    session_data = toml.loads(session_data_str)
    session_manager = SessionManager()
    ssh_command = session_manager.connect_ssh(session_data, session_name)

    return ssh_command


def list_sessions():
    config_manager = ConfigManager()
    session_names = config_manager.load_all_session_names()

    if not session_names:
        print("[ sshman : No sessions found. ]")
        return

    print("[ sshman: Available sessions: ]")
    for session_name in session_names:
        print(f"- {session_name}")

def get_installed_version():
    version_file = os.path.join(os.path.expanduser("~/.sshm/.bin/"), "version")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            content = f.read()
            return content
    return "Unknown"

def get_latest_version(user: str, repo: str):
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    response = get(url)
    if response.status_code == 200:
        release_data = response.json()
        vers = release_data["tag_name"]
        return vers
    return "Unknown"

def download_latest(user: str, repo: str, path="./"):
    os_name = platform.system().lower()
    if os_name not in ["linux", "windows"]:
        print(f"[ sshman: Unsupported OS '{os_name}'. Only Linux and Windows are supported. ]")
        return

    os_suffix = "linux" if os_name == "linux" else "win64"
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    response = get(url)
    ins_ver = get_installed_version()
    lat_ver = get_latest_version(gh_username, repository)

    if ins_ver == lat_ver:
        return print("[ sshman : You already have the latest version downloaded. ]")
    else:
        if response.status_code == 200:
            release_data = response.json()
            assets = release_data["assets"]

            # Find the correct asset for the user's OS
            asset = next((a for a in assets if os_suffix in a["name"].lower()), None)
            if not asset:
                print(f"[ sshman: No release found for {os_name}. ]")
                return

            download_url = asset["browser_download_url"]
            filename = os.path.join(path, asset["name"])

            with get(download_url, stream=True) as download_response:
                download_response.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in download_response.iter_content(chunk_size=8192):
                        f.write(chunk)

            print(f"[ sshman: Successfully downloaded {asset['name']} to {path} ]")
            downloaded_version = get_latest_version(gh_username, repository)
            with tarfile.open(filename, "r:gz") as tar:
                tar.extractall(path=path)

            extracted_folder = os.path.splitext(asset["name"])[0]
            extracted_sshman = os.path.join(path, "dist", "sshman")
            target_sshman = os.path.expanduser("~/.sshm/.bin/sshman")
            version_file = os.path.expanduser("~/.sshm/.bin/version")

            if os.path.exists(target_sshman):
                os.remove(target_sshman)
            if os.path.exists(version_file):
                os.remove(version_file)

            shutil.move(extracted_sshman, target_sshman)
            print("[ sshman: Moved binary to .sshm/.bin/ ]")

            version_file_path = os.path.join(os.path.expanduser("~/.sshm/.bin/"), "version")
            with open(version_file_path, "w") as vf:
                vf.write(downloaded_version)

            # Clean up the extracted folder
            shutil.rmtree(os.path.join(path, "dist/"))
            if os.path.exists(filename):
                os.remove(filename)
            print("[ sshman: Cleaned up extracted files. ]")
        else:
            print(f"[ sshman: Failed to fetch release data. Status code: {response.status_code} ]")

def main():
    parser = argparse.ArgumentParser(description="SSH Session Manager")
    parser.add_argument("-gs", "--generate-session", action="store_true", help="Generate a new SSH session")
    parser.add_argument("-rs", "--remove-session", type=str, help="Removes a session")
    parser.add_argument("-ls", "--sessions", help="Outputs all sessions", action="store_true")
    parser.add_argument("-c", "--connect", type=str, help="Connect to a saved SSH session by name")
    parser.add_argument("-v", "--version", action="store_true", help="Shows installed and latest version.")
    parser.add_argument("-u", "--update", help="Downloads the latest compiled version and installs it",
                        action="store_true")

    args = parser.parse_args()

    if args.generate_session:
        print("[ sshman : Generating sessiRejectPolicyon ]")
        generate_session()
    elif args.update:
        print(f"[ sshman : Downloading latest version of sshman... ]")
        download_latest(gh_username, repository, path="./")
    elif args.version:
        installed_version = get_installed_version()
        latest_version = get_latest_version(gh_username, repository)
        print(f"[ sshman : Installed version: {installed_version} | Latest version: {latest_version} ]")
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
