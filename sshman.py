#! /usr/bin/python3
from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO

from Assets.config_manager import ConfigManager
from Assets.session_manager import SessionManager
from Assets.version_manager import VersionManager

basicConfig(level=INFO, format="[%(levelname)s] %(message)s")
logger = getLogger("sshman")

GH_USERNAME, REPOSITORY = "auth-xyz", "sshman"

def main():
    parser = ArgumentParser(description="SSH Session Manager")
    parser.add_argument("-gs", "--generate-session", action="store_true", help="Generate a new SSH session")
    parser.add_argument("-rs", "--remove-session", type=str, help="Removes a session")
    parser.add_argument("-ls", "--sessions", help="Outputs all sessions", action="store_true")
    parser.add_argument("-c", "--connect", type=str, help="Connect to a saved SSH session by name")
    parser.add_argument("-v", "--version", action="store_true", help="Shows installed and latest version.")
    parser.add_argument("-u", "--update", help="Downloads the latest compiled version and installs it",
                        action="store_true")

    args = parser.parse_args()

    if args.generate_session:
        logger.info("[ sshman : Generating session ]")
        SessionManager.generate_session()
    elif args.update:
        logger.info(f"[ sshman : Downloading latest version of sshman... ]")
        VersionManager.download_latest(GH_USERNAME, REPOSITORY, path="./")
    elif args.version:
        installed_version = VersionManager.get_installed_version()
        latest_version = VersionManager.get_latest_version(GH_USERNAME, REPOSITORY)
        logger.info(f"[ sshman : Installed version: {installed_version} | Latest version: {latest_version} ]")
    elif args.connect:
        logger.info(f"[ sshman : Connecting to session '{args.connect}' ]")
        SessionManager.connect_session(args.connect)
    elif args.sessions:
        SessionManager.list_sessions()
    elif args.remove_session:
        logger.info(f"[ sshman : Removing session '{args.remove_session}' ]")
        config_manager = ConfigManager()
        config_manager.remove_session(args.remove_session)
    else:
        logger.error("[ sshman : No valid option selected. Use --help for usage details. ]")


if __name__ == "__main__":
    main()
