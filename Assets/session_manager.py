from toml import dump
from os import path, read
from select import select
from getpass import getpass
from sys import stdout, stdin
from base64 import b64encode, b64decode

from paramiko import RSAKey, AuthenticationException, SSHException, SSHClient
from paramiko.client import AutoAddPolicy

class SessionManager:
    @staticmethod
    def _encode_base64(data):
        return b64encode(data.encode()).decode()

    @staticmethod
    def _decode_base64(encoded_data):
        return b64decode(encoded_data).decode()

    @staticmethod
    def connect_ssh(session_info, session_name):
        username = session_info[f"main-{session_name}"]["username"]
        host = session_info[f"main-{session_name}"]["host"]
        key_path = session_info[f"main-{session_name}"].get("key", None)

        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy)

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

                    # Save the updated session_info to the .toml file with the corresponding session name
                    with open(session_file, "w") as toml_file:
                        dump(session_info, toml_file)

                client.connect(hostname=host, username=username, password=password, port=22)

            channel = client.get_transport().open_session()
            channel.get_pty()  # Request a pseudo-terminal (PTY) for terminal support

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
