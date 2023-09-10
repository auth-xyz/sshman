# SSH Session Manager

### A simple CLI tool to manage and connect to SSH clients.

#### Prerequisites:
*  [Python 3.10+](https://python.org/downloads/)
*  [Poetry 1.5+](https://github.com/python-poetry/poetry) (optional)

> [!NOTE]
> Of course you can also download the compiled binary from the [GitHub release page](https://github.com/auth-xyz/sshman/releases)


#### Building from source

```bash
# Cloning repository
git clone https://github.com/auth-xyz/sshman
cd sshman
# Installing dependencies
poetry install #using poetry
pip install toml paramiko httpx beautifulsoup4 #using pip

poetry run python build.py # Actually building
```
#### Installation (Linux)
```bash
# Easy way
curl -L "https://raw.githubusercontent.com/auth-xyz/sshman/main/Bin/linux_install.sh" | bash

# Manual way:
# Download the latest binary from the release page
tar xfz linux-<version>.tar.gz
mkdir -p $HOME/.sshm/.bin
mv sshman $HOME/.sshm/.bin

sudo ln -s $HOME/.sshm/.bin/sshman /usr/bin/  
```

#### General Usage
```bash
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
