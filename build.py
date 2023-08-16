#!/usr/bin/env python3

from logging import basicConfig, getLogger, INFO
from shutil import rmtree
from platform import system
from pathlib import Path
from tarfile import open

basicConfig(level=INFO, format="[%(levelname)s] %(message)s")
logger = getLogger("sshman")

root_path = Path(__file__).parent
system = system()

version = "snow-dome"
binary_name = "sshman"
output_tar = f"{version}.tar.gz"


def run_pyinstaller(args):
    from PyInstaller.__main__ import run
    run(args + ["main.py"])


def create_tar_gz(filename, files):
    archive_root = files[0].parent
    with open(filename, "w:gz") as tar:
        for file in files:
            arcname = file.relative_to(archive_root)
            tar.add(file, arcname=arcname)


def cleanup():
    dist_path = root_path / "dist"
    build_path = root_path / "build"
    spec_file = root_path / f"{binary_name}.spec"

    rmtree(dist_path, ignore_errors=True)
    rmtree(build_path, ignore_errors=True)
    spec_file.unlink(missing_ok=True)


if __name__ == "__main__":
    pyinstaller_args = ["--onefile", "--name", binary_name]
    run_pyinstaller(pyinstaller_args)

    binary_path = root_path / "dist" / binary_name
    create_tar_gz(output_tar, [binary_path])

    cleanup()

    logger.info(f"sshman : Finished compilation, output file: {output_tar}")
