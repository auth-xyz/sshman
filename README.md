# SSH Session Manager

### A simple Python-based SSH session manager to facilitate easy connection to SSH hosts. This project allows you to generate, connect, list, and remove SSH sessions by saving them as TOML files.


#### Prerequisites:
> [Python 3.10+](https://python.org/downloads/)

#### Installation:

```bash
git clone https://github.com/auth-xyz/sshman
cd sshman/
pip install -r requirements.txt
```

##### Otherwise, you can download the compiled [version](https://github.com/auth-xyz/sshman/releases/)

#### Usage:

* Generating Session:
```bash
python sshman.py --generate-session
```

* Removing Session
```bash
python sshman.py --remove-session <session-name>
```

* Connecting to a session
```bash
python sshman.py --connect <session-name>
```

* Listing all sessions
```bash
python sshman.py --sessions
```


###### sshman, is a side project of mine that I decided to work on after thinking about it for a while, its a simple program that can be set up with 2 lines.

