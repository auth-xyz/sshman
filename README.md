# sshman - A easy to use SSH Manager.

##### sshman, is a side project of mine that I decided to work on after thinking about it for a while, its a simple program that can be setted up with 2 lines.

##### For now, i've only tested sshman on Arch, it still needs some work to be put into it, for its still not finished. But I'll do what I can to get it working.

## Installation:

#### Requirements:
> [Python 3.10+](https://python.org/downloads/)

```bash
# Clone the repository
git clone https://github.com/auth-xyz/sshman
cd sshman/

chmod +x sshman.py # Lets you do ./sshman.py instead of having to run python3 sshman.py, etc.
sudo ln -s /path/to/sshman/sshman.py /usr/bin/sshman # lets you use sshman in whatever directory you are

## Basic usage:
# to create a session you can do:
sshman --generate-session
# After answering a few questions, a folder in $HOME will be created .sshm
# In there will be saved your sessions.

# to connect to a session, you can run:
sshman --connect <session>

# To list the sessions you have, you can use:
sshman --sessions

# To remove a session you generated you can use
sshman --remove-session <session>

# A note about --generate-session:
# username : the username of the machine you're connecting to via ssh
# host : the machine's public ipv4
# key-path (if you use a key like a .pem) : put the entire path, ex: /home/auth/.ssh/key.pem. If you don't have a key, you can leave this empty.
```

