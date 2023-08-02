#!/usr/bin/env bash

version="mount-temple"

build_windows() {
    wine pyinstaller --onefile sshman.py
    rm -rf build *.spec
    cd dist/
    cat ../Bin/win_install.bat >> ./install.bat
    chmod +x sshman.exe
    cd ..
    tar cfz "win64-$version.tar.gz" dist/*
    echo "[ sshman : Windows building process was finished ]"
}

build_linux() {
    pyinstaller --onefile sshman.py
    rm -rf build *.spec
    cd dist/
    cat ../Bin/linux_install.sh >> ./install.sh
    chmod +x install.sh
    chmod +x sshman
    cd ..
    tar cfz "linux-$version.tar.gz" dist/*
    echo "[ sshman : Linux building process was finished ]"
}

clean_up() {
    rm -rf dist/
}

build_windows
clean_up
sleep 1
build_linux
clean_up

mv "win64-$version.tar.gz" "linux-$version.tar.gz" ~/Downloads/
echo "[ sshman : All building processes were finished ]"
