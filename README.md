# SSH Session Manager

### A simple Python-based SSH session manager to facilitate easy connection to SSH hosts. This project allows you to generate, connect, list, and remove SSH sessions by saving them as TOML files.


#### Prerequisites:
> [Python 3.10+](https://python.org/downloads/)

> [!NOTE]
> You can download the binary release for ease of use [here](https://github.com/auth-xyz/sshman/releases)


#### Installation:

```bash
git clone https://github.com/auth-xyz/sshman
cd sshman/
pip install -r requirements.txt
```

#### Usage:

* Generating Session:
```bash
python main.py --generate-session
```

* Removing Session
```bash
python main.py --remove-session <session-name>
```

* Connecting to a session
```bash
python main.py --connect <session-name>
```

* Listing all sessions
```bash
python main.py --sessions
```


###### sshman, is a side project of mine that I decided to work on after thinking about it for a while, it's a simple program that can be set up with 2 lines.

