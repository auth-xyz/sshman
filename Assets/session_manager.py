from subprocess import run, TimeoutExpired

from toml import dump, loads, dumps
from tty import setraw
from os import path, read
from select import select
from getpass import getpass
from sys import stdout, stdin
from base64 import b64encode, b64decode

from paramiko import RSAKey, AuthenticationException, SSHException, SSHClient
from paramiko.client import RejectPolicy

from Assets.config_manager import ConfigManager
from logging import basicConfig, getLogger, INFO

basicConfig(level=INFO, format="[%(levelname)s] %(message)s")
logger = getLogger("sshman")


class SessionManager:
    @staticmethod
    def _encode_base64(data):
        return b64encode(data.encode()).decode()

    @staticmethod
    def _decode_base64(encoded_data):
        return b64decode(encoded_data).decode()

    @staticmethod
    def is_host_up(host):
        try:
            response = run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
            return response.returncode == 0
        except TimeoutExpired:
            return False

    @staticmethod
    def generate_session():
        session_name = input("sshman : how do you want to name this session? ")
        username = input("sshman : input the username: ")
        host = input("sshman : input the host: ")
        key_path = input("sshman : input the key path (leave blank for password authentication): ")

        if not session_name:
            print("Session name cannot be empty.")
            return

        if not username:
            print("Username cannot be empty.")
            return

        if not host:
            print("Host cannot be empty.")
            return

        if not SessionManager.is_host_up(host):
            user_choice = input("Host is not reachable. Do you want to continue generating the session? (y/n): ")
            if user_choice.lower() != "y":
                return


        session_data = {
            "username": username,
            "host": host,
            "key": key_path if key_path else None,
        }

        session_data_str = dumps({"main-" + session_name: session_data})
        config_manager = ConfigManager()
        config_manager.create_config_directory()
        config_manager.save_session_info(session_name, session_data_str)

        print("Success!")

    @staticmethod
    def connect_session(session_name):
        config_manager = ConfigManager()
        session_data_str = config_manager.load_session_info(session_name)
        if not session_data_str:
            print(f"sshman : Session '{session_name}' not found.")
            return

        session_data = loads(session_data_str)
        SessionManager.connect_ssh(session_data, session_name)

    @staticmethod
    def list_sessions():
        config_manager = ConfigManager()
        session_names = config_manager.load_all_session_names()

        if not session_names:
            print("[ sshman : No sessions found. ]")
            return

        print("[ sshman: Available sessions: ]\n")
        for session_name in session_names:
            print(f"[-> {session_name} ]")

    @staticmethod
    def connect_ssh(session_info, session_name):
        username = session_info[f"main-{session_name}"]["username"]
        host = session_info[f"main-{session_name}"]["host"]
        key_path = session_info[f"main-{session_name}"].get("key", None)

        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(RejectPolicy)

        try:
            saved_password = session_info[f"main-{session_name}"].get("password", None)

            if key_path:
                key = RSAKey.from_private_key_file(key_path)
                client.connect(hostname=host, username=username, pkey=key, port=22)
            elif saved_password:
                password = SessionManager._decode_base64(saved_password)
                client.connect(hostname=host, username=username, password=password, port=22)
            else:
                password = getpass("[ sshman : Input your password ] ")
                save_password = input("[ sshman : Save password for future sessions? (y/n) ] ").lower()

                if save_password == "y":
                    encoded_password = SessionManager._encode_base64(password)
                    session_info[f"main-{session_name}"]["password"] = encoded_password
                    config_dir = path.expanduser(path.join("~", ".sshm"))
                    session_file = path.join(config_dir, f"{session_name}.toml")

                    with open(session_file, "w") as toml_file:
                        dump(session_info, toml_file)

                client.connect(hostname=host, username=username, password=password, port=22)

            channel = client.get_transport().open_session()
            channel.get_pty()
            setraw(stdin.fileno())  # This line breaks win64 binaries, I'll eventually try to fix it.

            channel.exec_command("bash")

            while True:
                r, _, _ = select([channel, stdin], [], [])
                if channel in r:
                    output = channel.recv(1024).decode()
                    if not output:
                        break
                    stdout.write(output)
                    stdout.flush()
                if stdin in r:
                    input_data = read(stdin.fileno(), 1024)
                    if not input_data:
                        break
                    channel.sendall(input_data)

            channel.close()

        except AuthenticationException:
            print("[ sshman : Authentication failed. ]")
        except SSHException as e:
            print(f"[ sshman : SSH error: {e} ]")
        except Exception as e:
            print(f"[ sshman : Error: {e} ]")
        finally:
            client.close()

