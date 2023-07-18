import paramiko

class SessionManager:
    def connect_ssh(self, session_info, session_name):
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
                client.connect(hostname=host, username=username)

            # Start an interactive shell session
            channel = client.invoke_shell()

            # Wait for the shell to be ready to receive commands
            while not channel.recv_ready():
                pass

            # Now you can interact with the shell as if you were typing commands manually
            while True:
                command = input("$ ")  # Prompt the user for a command
                if command.lower() == "exit":
                    break

                # Send the command to the remote shell
                channel.send(command + '\n')

                # Wait for the command to execute and receive the output
                while not channel.recv_ready():
                    pass
                output = channel.recv(4096).decode()

                # Print the output
                print(output)

            # Close the SSH channel
            channel.close()

        except paramiko.AuthenticationException:
            print("[ sshman : Authentication failed. ]")
        except paramiko.SSHException as e:
            print(f"[ sshman : SSH error: {e} ]")
        except Exception as e:
            print(f"[ sshman : Error: {e} ]")
        finally:
            client.close()
            