#!/bin/bash

# Define variables for paths
INSTALL_DIR="$HOME/.sshm/.bin"
BIN_NAME="sshman"

# Check for dependencies
if ! command -v cp >/dev/null; then
    echo "Error: 'cp' command not found. Please install 'coreutils' package."
    exit 1
fi

if ! command -v sudo >/dev/null; then
    echo "Error: 'sudo' command not found. Please make sure you have sudo access."
    exit 1
fi

# Display informative message
echo "[ sshman : Installing ]"
mkdir -p "$INSTALL_DIR"
cp "./$BIN_NAME" "$INSTALL_DIR/"

sudo ln -sf "$INSTALL_DIR/$BIN_NAME" "/usr/local/bin/$BIN_NAME"

if [ $? -eq 0 ]; then
    echo "[ sshman : Installation completed successfully. You can now use 'sshman'. ]"
else
    echo "Error occurred during installation. Please try again."
    exit 1
fi
