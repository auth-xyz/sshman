from toml import dump
from tty import setraw
from os import path, read
from select import select
from getpass import getpass
from sys import stdout, stdin
from termios import tcgetattr
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
        key_path = session_info[f"main-{session_name}"].get("key", None)  # Use get() with a default value

        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy)

        try:
            password = None
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
                    # Encode the password in Base64 before saving it to the .toml file
                    encoded_password = SessionManager._encode_base64(password)
                    session_info[f"main-{session_name}"]["password"] = encoded_password
                    config_dir = path.expanduser(path.join("~", ".sshm"))
                    session_file = path.join(config_dir, f"{session_name}.toml")

                    # Save the updated session_info to the .toml file with the corresponding session name
                    with open (session_file, "w") as toml_file:
                        dump(session_info, toml_file)

                client.connect(hostname=host, username=username, password=password, port=22)

            channel = client.get_transport().open_session()
            channel.get_pty()  # Request a pseudo-terminal (PTY) for terminal support

            # Now, let's set the terminal attributes of the local terminal to match the remote terminal
            original_attrs = tcgetattr(stdin)
            setraw(stdin.fileno())

            # Let's interact with the remote shell using the PTY channel
            channel.exec_command("bash")  # Start an interactive bash shell

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
