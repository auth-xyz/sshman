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
    parser.add_argument("-is", "--import-session", type=str, help="Imports an exported session")
    parser.add_argument("-es", "--export-session", type=str, help="Exports a generated session")
    parser.add_argument("-ls", "--sessions", help="Outputs all sessions", action="store_true")
    parser.add_argument("-c", "--connect", type=str, help="Connect to a saved SSH session by name")
    parser.add_argument("-i", "--info", type=str, help="Outputs the session info")
    parser.add_argument("-v", "--version", action="store_true", help="Shows installed and latest version.")
    parser.add_argument("-u", "--update", help="Downloads the latest compiled version and installs it",
                        action="store_true")

    args = parser.parse_args()

    action_handlers = {
        'generate_session': SessionManager.generate_session,
        'info': lambda: SessionManager.show_session(args.info),
        'update': lambda: VersionManager.download_latest(GH_USERNAME, REPOSITORY, path="./"),
        'version': lambda: show_version(),
        'connect': lambda: connect_session(args.connect),
        'sessions': SessionManager.list_sessions,
        'remove_session': lambda: remove_session(args.remove_session),
        'export_session': lambda: export_session(args.export_session),
        'import_session': lambda: import_session(args.import_session),
    }

    selected_action = None
    for action, value in vars(args).items():
        if value:
            selected_action = action
            break

    action_handler = action_handlers.get(selected_action, lambda: logger.error(
        "[ sshman : No valid option selected. Use --help for usage details. ]"))
    action_handler()


def show_version():
    installed_version = VersionManager.get_installed_version()
    latest_version = VersionManager.get_latest_version(GH_USERNAME, REPOSITORY)
    logger.info(f"[ sshman : Installed version: {installed_version} | Latest version: {latest_version} ]")


def connect_session(session_name):
    sm = SessionManager()
    logger.info(f"[ sshman : Connecting to session '{session_name}' ]")
    sm.connect_session(session_name)


def remove_session(session_name):
    logger.info(f"[ sshman : Removing session '{session_name}' ]")
    config_manager = ConfigManager()
    config_manager.remove_session(session_name)


def export_session(session_name):
    config_manager = ConfigManager()
    config_manager.export_session_info(session_name=f"{session_name}", export_dir="./")


def import_session(import_file):
    config_manager = ConfigManager()
    config_manager.import_session_info(session_name=f"{import_file}", import_file=f"./{import_file}")


if __name__ == "__main__":
    main()
