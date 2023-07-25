# SSH Session Manager

### En simpel SSH-sessionmanager baseret på Python, der letter nem forbindelse til SSH-værter. Dette projekt giver dig mulighed for at generere, forbinde, liste og fjerne SSH-sessioner ved at gemme dem som TOML-filer.

#### Forudsætninger:
> [Python 3.10+](https://python.org/downloads/)

#### Installation:

```bash
git clone https://github.com/auth-xyz/sshman
cd sshman/
pip install -r requirements.txt
```

Alternativt kan du downloade den kompilerede version
Brug:

* Generer session:
```
python sshman.py --generate-session
```

* Fjern session:
```
python sshman.py --remove-session <session-navn>
```

* Forbind til en session:
```
python sshman.py --connect <session-navn>
```

* Vis alle sessioner:
```
python sshman.py --sessions
```