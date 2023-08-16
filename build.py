#! /usr/bin/python3

import platform

from pathlib import Path
from PyInstaller.__main__ import run

root_path = Path(__file__).parent.parent
system = platform.system()

args = ["--onefile"]

run(args + ["./main.py"])
