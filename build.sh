#! /usr/bin/bash

version="mount-temple"

# Windows
wine pyinstaller --onefile sshman.py
rm -rf build
# shellcheck disable=SC2035
rm *.spec

# shellcheck disable=SC2164
cd dist/
cat ../Bin/win_install.bat >> ./install.bat
chmod +x sshman
# shellcheck disable=SC2103
cd ..

tar cfz win64-$version.tar.gz dist/*
clear
# shellcheck disable=SC2035
mv *.tar.gz ~/Downloads/
echo "[ sshman : Windows building process was finished ]"

# Clean up for Linux build
rm -rf dist/

# Linux
pyinstaller --onefile sshman.py
rm -rf build
rm *.spec

# shellcheck disable=SC2164
cd dist/
cat ../Bin/linux_install.sh >> ./install.sh
chmod +x install.sh
chmod +x sshman
cd ..

tar cfz linux-$version.tar.gz dist/*
clear
# shellcheck disable=SC2035
mv *.tar.gz ~/Downloads/
echo "[ sshman : Linux building process was finished ]"
