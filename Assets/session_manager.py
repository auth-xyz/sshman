import paramiko

class SessionManager:
    def connect_ssh(self, session_info):
        username = session_info.get("username", "")
        host = session_info.get("host", "")
        key_path = session_info.get("key", "")

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        try:
            if key_path:
                key = paramiko.RSAKey.from_private_key_file(key_path)
                client.connect(hostname=host, username=username, pkey=key)
            else:
                client.connect(hostname=host, username=username)

            # Execute your SSH commands here if needed.
            stdin, stdout, stderr = client.exec_command("ls -al")
            print(stdout.read().decode())

        except paramiko.AuthenticationException:
            print("sshman : Authentication failed.")
        except paramiko.SSHException as e:
            print(f"sshman : SSH error: {e}")
        except Exception as e:
            print(f"sshman : Error: {e}")
        finally:
            client.close()
            