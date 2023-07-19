import paramiko
import os
import sys
import tty
import termios
import select

class SessionManager:
    @staticmethod
    def connect_ssh(session_info, session_name):
        username = session_info[f"main-{session_name}"]["username"]
        host = session_info[f"main-{session_name}"]["host"]
        key_path = session_info[f"main-{session_name}"]["key"]

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        try:
            if key_path:
                key = paramiko.RSAKey.from_private_key_file(key_path)
                client.connect(hostname=host, username=username, pkey=key)
            else:
                password = input("[ sshman : Input your password ] ")
                client.connect(hostname=host, username=username, password=password)

            channel = client.get_transport().open_session()
            channel.get_pty()  # Request a pseudo-terminal (PTY) for terminal support

            # Now, let's set the terminal attributes of the local terminal to match the remote terminal
            original_attrs = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())

            # Let's interact with the remote shell using the PTY channel
            channel.exec_command("bash")  # Start an interactive bash shell

            while True:
                r, _, _ = select.select([channel, sys.stdin], [], [])
                if channel in r:
                    output = channel.recv(1024).decode()
                    if not output:
                        break
                    sys.stdout.write(output)
                    sys.stdout.flush()
                if sys.stdin in r:
                    input_data = os.read(sys.stdin.fileno(), 1024)
                    if not input_data:
                        break
                    channel.sendall(input_data)

            channel.close()

        except paramiko.AuthenticationException:
            print("[ sshman : Authentication failed. ]")
        except paramiko.SSHException as e:
            print(f"[ sshman : SSH error: {e} ]")
        except Exception as e:
            print(f"[ sshman : Error: {e} ]")
        finally:
            client.close()
