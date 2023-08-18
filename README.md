# SSH Session Manager

### A simple CLI tool to manage and connect to SSH clients.

#### Prerequisites:
*  [Python 3.10+](https://python.org/downloads/)
*  [Poetry 1.5+](https://github.com/python-poetry/poetry) (optional)


#### Building from source

```bash
# Cloning repository
git clone https://github.com/auth-xyz/sshman
cd sshman
# Installing dependecies
poetry install #using poetry
pip install toml paramiko httpx beautifulsoup4 #using pip

poetry run python build.py # Actually building
```
#### Installation (Linux)
```bash
tar xfz <version>.tar.gz

# First way
sudo ln -s path/to/sshman /usr/bin/sshman
# Easier way
sudo mv path/to/sshman /usr/bin/
```

> [!NOTE]
> Of course you can also download the binary from the [github release page](https://github.com/auth-xyz/sshman/releases)

#### Usage
###### (this uses the already installed binary, it may be different in your case.)
```
# Generating session
sshman -gs
sshman --generate-session

# Removing a generated session
sshman -rs <session>
sshman --remove-session <session>

# Connecting to a session
sshman -c <session> --safe #default
sshman --connect <session> --unsafe # unsafe is when you haven't connected to this server yet

# Other helpful commands that are self-explained
sshman -ls / --list-sessions 
sshman -u / --update
sshman -v / --version
```

###### If you'd like to contribute, feel free to do so!